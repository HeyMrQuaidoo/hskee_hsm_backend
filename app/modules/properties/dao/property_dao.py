from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import UUID4
from fastapi import UploadFile

# Models
from app.modules.properties.models.property import Property
from app.modules.resources.models.media import Media
from app.modules.associations.models.entity_media import EntityMedia

# Enums
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum

# DAOs for relationships
from app.modules.address.dao.address_dao import AddressDAO
from app.modules.properties.dao.unit_dao import UnitDAO
from app.modules.resources.dao.media_dao import MediaDAO
from app.modules.resources.dao.amenity_dao import AmenityDAO
from app.modules.billing.dao.utility_dao import UtilityDAO

# Base DAO
from app.modules.common.dao.base_dao import BaseDAO

# Core
from app.core.errors import RecordNotFoundException

# Services
from app.services.upload_service import MediaUploaderService

class PropertyDAO(BaseDAO[Property]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Property

        # DAOs for related entities
        self.address_dao = AddressDAO()
        self.unit_dao = UnitDAO()
        self.media_dao = MediaDAO()
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
                "is_thumbnail": is_thumbnails[idx] if is_thumbnails and idx < len(is_thumbnails) else False,
                "caption": captions[idx] if captions and idx < len(captions) else None,
                "description": descriptions[idx] if descriptions and idx < len(descriptions) else None,
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
