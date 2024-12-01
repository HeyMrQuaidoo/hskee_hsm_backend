from typing import Optional, List
from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

# Models
from app.core.response import DAOResponse
from app.modules.properties.models.property import Property
from app.modules.properties.enums.property_enums import PropertyType, PropertyStatus

# DAOs
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.properties.dao.unit_dao import UnitDAO
from app.modules.resources.dao.media_dao import MediaDAO
from app.modules.billing.dao.utility_dao import UtilityDAO
from app.modules.address.dao.address_dao import AddressDAO
from app.modules.resources.dao.amenity_dao import AmenityDAO

# Core
from app.core.errors import CustomException, RecordNotFoundException

# Services
from fastapi import UploadFile
from app.services.upload_service import MediaUploaderService
from app.modules.associations.models.entity_media import EntityMedia
from app.modules.resources.models.media import Media
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


class PropertyDAO(BaseDAO[Property]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Property

        self.unit_dao = UnitDAO()
        self.media_dao = MediaDAO()
        self.address_dao = AddressDAO()
        self.amenity_dao = AmenityDAO()
        self.utility_dao = UtilityDAO()

        self.detail_mappings = {
            "address": self.address_dao,
            "units": self.unit_dao,
            "media": self.media_dao,
            "amenities": self.amenity_dao,
            "utilities": self.utility_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="property_unit_assoc_id",
        )

    async def get_properties(
        self,
        db_session: AsyncSession,
        name: Optional[str] = None,
        property_type: Optional[PropertyType] = None,
        amount_gte: Optional[float] = None,
        amount_lte: Optional[float] = None,
        floor_space_gte: Optional[float] = None,
        floor_space_lte: Optional[float] = None,
        num_units: Optional[int] = None,
        num_bathrooms: Optional[int] = None,
        num_garages: Optional[int] = None,
        has_balconies: Optional[bool] = None,
        has_parking_space: Optional[bool] = None,
        pets_allowed: Optional[bool] = None,
        property_status: Optional[PropertyStatus] = None,
        is_contract_active: Optional[bool] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            query = select(self.model)

            filter_conditions = {
                "name": self.model.name.ilike(f"%{name}%") if name else None,
                "property_type": self.model.property_type == property_type
                if property_type
                else None,
                "amount_gte": self.model.amount >= amount_gte
                if amount_gte is not None
                else None,
                "amount_lte": self.model.amount <= amount_lte
                if amount_lte is not None
                else None,
                "floor_space_gte": self.model.floor_space >= floor_space_gte
                if floor_space_gte is not None
                else None,
                "floor_space_lte": self.model.floor_space <= floor_space_lte
                if floor_space_lte is not None
                else None,
                "num_units": self.model.num_units == num_units
                if num_units is not None
                else None,
                "num_bathrooms": self.model.num_bathrooms == num_bathrooms
                if num_bathrooms is not None
                else None,
                "num_garages": self.model.num_garages == num_garages
                if num_garages is not None
                else None,
                "has_balconies": self.model.has_balconies == has_balconies
                if has_balconies is not None
                else None,
                "has_parking_space": self.model.has_parking_space == has_parking_space
                if has_parking_space is not None
                else None,
                "pets_allowed": self.model.pets_allowed == pets_allowed
                if pets_allowed is not None
                else None,
                "property_status": self.model.property_status == property_status
                if property_status
                else None,
                "is_contract_active": self.model.is_contract_active
                == is_contract_active
                if is_contract_active is not None
                else None,
            }

            filters = [
                condition
                for condition in filter_conditions.values()
                if condition is not None
            ]

            if filters:
                query = query.where(and_(*filters))

            query = query.order_by(self.model.name.asc())

            total_query = select(func.count()).select_from(query.subquery())
            query = query.limit(limit).offset(offset)

            result = await db_session.execute(query)
            properties = result.scalars().all()

            total_items_result = await db_session.execute(total_query)
            total_count = total_items_result.scalar()

            meta = {
                "total_items": total_count,
                "limit": limit,
                "offset": offset,
            }

            return DAOResponse(success=True, data=properties, meta=meta)
        except Exception as e:
            raise CustomException(str(e))

    async def upload_media(
        self,
        property_id: str,
        files: List[UploadFile],
        descriptions: Optional[List[str]],
        captions: Optional[List[str]],
        is_thumbnails: Optional[List[bool]],
        db_session: AsyncSession,
    ):
        # Check if property exists
        property = await self.get(db_session=db_session, id=property_id)
        if not property:
            raise RecordNotFoundException(model="Property", id=property_id)

        for idx, file in enumerate(files):
            content = await file.read()
            base64_image = f"data:{file.content_type};base64,{content.decode('latin1')}"
            file_name = file.filename
            media_type_str = "property"

            # Use MediaUploaderService
            uploader = MediaUploaderService(base64_image, file_name, media_type_str)
            response = uploader.upload()

            if not response.success:
                raise Exception(f"Upload failed: {response.error}")

            # Determine media type based on file content type
            content_type = file.content_type
            if "image" in content_type:
                media_type = MediaType.image
            elif "video" in content_type:
                media_type = MediaType.video
            elif "audio" in content_type:
                media_type = MediaType.audio
            elif "application" in content_type:
                media_type = MediaType.document
            else:
                media_type = MediaType.other

            # Create Media instance
            media_data = {
                "media_name": file_name,
                "media_type": media_type,
                "content_url": response.data["content_url"],
                "is_thumbnail": is_thumbnails[idx]
                if is_thumbnails and idx < len(is_thumbnails)
                else False,
                "caption": captions[idx] if captions and idx < len(captions) else None,
                "description": descriptions[idx]
                if descriptions and idx < len(descriptions)
                else None,
            }
            await self.add_media_to_property(
                db_session=db_session,
                property_id=property_id,
                media_data=media_data,
            )

    async def add_media_to_property(
        self,
        db_session: AsyncSession,
        property_id: str,
        media_data: dict,
    ):
        # Create Media instance
        media = Media(**media_data)
        db_session.add(media)
        await db_session.flush()

        # Create EntityMedia association
        entity_media = EntityMedia(
            media_id=media.media_id,
            entity_id=property_id,
            entity_type=EntityTypeEnum.property,
            media_type=media.media_type,
        )
        db_session.add(entity_media)
        await db_session.commit()
