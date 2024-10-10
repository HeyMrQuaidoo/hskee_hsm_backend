import logging

from typing import List, Optional
from pydantic import UUID4
from fastapi import Depends, File, UploadFile, status, Form, Query
from sqlalchemy.ext.asyncio import AsyncSession

# DAO imports
from app.modules.properties.dao.property_dao import PropertyDAO

# Schema imports
from app.modules.common.router.base_router import BaseCRUDRouter
from app.modules.common.schema.schemas import PropertySchema
from app.modules.properties.schema.property_schema import (
    PropertyCreateSchema,
    PropertyUpdateSchema,
)
from app.modules.resources.schema.amenities_schema import AmenitySchema
from app.modules.resources.schema.media_schema import MediaSchema
from app.modules.billing.schema.utility_schema import UtilitySchema
from app.modules.billing.schema.entity_billable import (
    EntityBillableSchema,
    EntityBillableUpdateSchema,
)

# Core imports
from app.core.lifespan import get_db
from app.core.response import DAOResponse
from app.core.errors import CustomException

# Enums
from app.modules.resources.enums.resource_enums import MediaType

import cloudinary.uploader


class PropertyRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        self.dao: PropertyDAO = PropertyDAO(excludes=[])
        super().__init__(dao=self.dao, schemas=PropertySchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post(
            "/{property_id}/amenities", status_code=status.HTTP_201_CREATED
        )
        async def add_amenities_to_property(
            property_id: UUID4,
            amenity_ids: List[UUID4],
            apply_to_units: bool = Query(False),
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                response = await self.dao.add_amenities(
                    db_session=db_session,
                    property_id=property_id,
                    amenity_ids=amenity_ids,
                    apply_to_units=apply_to_units,
                )
                return response
            except Exception as e:
                raise CustomException(str(e))

        @self.router.get(
            "/{property_id}/amenities", response_model=List[AmenitySchema]
        )
        async def get_property_amenities(
            property_id: UUID4, db_session: AsyncSession = Depends(get_db)
        ):
            try:
                amenities = await self.dao.get_amenities(
                    db_session=db_session, property_id=property_id
                )
                return [AmenitySchema.model_validate(a) for a in amenities]
            except Exception as e:
                raise CustomException(str(e))

        @self.router.delete(
            "/{property_id}/amenities/{amenity_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        async def remove_amenity_from_property(
            property_id: UUID4,
            amenity_id: UUID4,
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                await self.dao.remove_amenity(
                    db_session=db_session,
                    property_id=property_id,
                    amenity_id=amenity_id,
                )
            except Exception as e:
                raise CustomException(str(e))

        @self.router.post("/{property_id}/media", status_code=status.HTTP_201_CREATED)
        async def upload_media_to_property(
            property_id: UUID4,
            files: List[UploadFile] = File(...),
            descriptions: Optional[List[str]] = Form(None),
            captions: Optional[List[str]] = Form(None),
            is_thumbnails: Optional[List[bool]] = Form(None),
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                media_list = []
                for idx, file in enumerate(files):
                    # Upload to Cloudinary
                    result = cloudinary.uploader.upload(file.file)
                    uploaded_url = result["secure_url"]

                    # Determine media type
                    content_type = file.content_type
                    if "image" in content_type:
                        media_type = MediaType.image
                    elif "video" in content_type:
                        media_type = MediaType.video
                    else:
                        media_type = MediaType.document

                    # Get description, caption, is_thumbnail from request
                    description = (
                        descriptions[idx]
                        if descriptions and idx < len(descriptions)
                        else None
                    )
                    caption = (
                        captions[idx] if captions and idx < len(captions) else None
                    )
                    is_thumbnail = (
                        is_thumbnails[idx]
                        if is_thumbnails and idx < len(is_thumbnails)
                        else False
                    )

                    # Prepare media data
                    media_data = {
                        "content_url": uploaded_url,
                        "media_name": file.filename,
                        "media_type": media_type,
                        "description": description,
                        "caption": caption,
                        "is_thumbnail": is_thumbnail,
                    }

                    media_list.append(media_data)

                response = await self.dao.add_media(
                    db_session=db_session,
                    property_id=property_id,
                    media_list=media_list,
                )
                return response
            except Exception as e:
                raise CustomException(str(e))

        @self.router.get("/{property_id}/media", response_model=List[MediaSchema])
        async def get_property_media(
            property_id: UUID4, db_session: AsyncSession = Depends(get_db)
        ):
            try:
                media_items = await self.dao.get_media(
                    db_session=db_session, property_id=property_id
                )
                return [MediaSchema.model_validate(m) for m in media_items]
            except Exception as e:
                raise CustomException(str(e))

        @self.router.delete(
            "/{property_id}/media/{media_id}", status_code=status.HTTP_204_NO_CONTENT
        )
        async def remove_media_from_property(
            property_id: UUID4,
            media_id: UUID4,
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                await self.dao.remove_media(
                    db_session=db_session,
                    property_id=property_id,
                    media_id=media_id,
                )
            except Exception as e:
                raise CustomException(str(e))

        @self.router.post(
            "/{property_id}/utilities", status_code=status.HTTP_201_CREATED
        )
        async def add_utilities_to_property(
            property_id: UUID4,
            utilities: List[UtilitySchema],
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                response = await self.dao.add_utilities(
                    db_session=db_session,
                    property_id=property_id,
                    utilities=utilities,
                )
                return response
            except Exception as e:
                raise CustomException(str(e))

        @self.router.get(
            "/{property_id}/utilities", response_model=List[UtilitySchema]
        )
        async def get_property_utilities(
            property_id: UUID4, db_session: AsyncSession = Depends(get_db)
        ):
            try:
                utilities = await self.dao.get_utilities(
                    db_session=db_session, property_id=property_id
                )
                return [UtilitySchema.model_validate(u) for u in utilities]
            except Exception as e:
                raise CustomException(str(e))

        @self.router.delete(
            "/{property_id}/utilities/{utility_id}",
            status_code=status.HTTP_204_NO_CONTENT,
        )
        async def remove_utility_from_property(
            property_id: UUID4,
            utility_id: UUID4,
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                await self.dao.remove_utility(
                    db_session=db_session,
                    property_id=property_id,
                    utility_id=utility_id,
                )
            except Exception as e:
                raise CustomException(str(e))
            

        @self.router.get(
                "/{property_id}/utilities/{utility_id}/billable",
                response_model=EntityBillableSchema,
            )
        async def get_utility_billable_details(
                property_id: UUID4,
                utility_id: UUID4,
                db_session: AsyncSession = Depends(get_db),
            ):
                try:
                    billable = await self.dao.get_utility_billable_details(
                        db_session=db_session,
                        property_id=property_id,
                        utility_id=utility_id,
                    )
                    return EntityBillableSchema.model_validate(billable)
                except Exception as e:
                    raise CustomException(str(e))

        @self.router.put(
            "/{property_id}/utilities/{utility_id}/billable",
            response_model=EntityBillableSchema,
        )
        async def update_utility_billable_details(
                property_id: UUID4,
                utility_id: UUID4,
                billable_update: EntityBillableUpdateSchema,
                db_session: AsyncSession = Depends(get_db),
            ):
                try:
                    billable = await self.dao.update_utility_billable_details(
                        db_session=db_session,
                        property_id=property_id,
                        utility_id=utility_id,
                        billable_update=billable_update,
                    )
                    return EntityBillableSchema.model_validate(billable)
                except Exception as e:
                    raise CustomException(str(e))
