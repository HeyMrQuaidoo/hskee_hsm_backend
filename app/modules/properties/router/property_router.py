from typing import List, Optional
from pydantic import UUID4
from fastapi import Depends, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.properties.dao.property_dao import PropertyDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import PropertySchema
from app.modules.properties.schema.property_schema import (
    PropertyCreateSchema,
    PropertyUpdateSchema,
    PropertyResponse,
)

# Core
from app.core.lifespan import get_db
from app.core.errors import CustomException


class PropertyRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: PropertyDAO = PropertyDAO(excludes=[])
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        PropertySchema["response_schema"] = PropertyResponse

        super().__init__(dao=self.dao, schemas=PropertySchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post(
            "/{property_id}/upload-media", status_code=status.HTTP_201_CREATED
        )
        async def upload_media_to_property(
            property_id: UUID4,
            files: List[UploadFile] = File(...),
            descriptions: Optional[List[str]] = Form(None),
            captions: Optional[List[str]] = Form(None),
            is_thumbnails: Optional[List[bool]] = Form(None),
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                await self.dao.upload_media(
                    property_id=str(property_id),
                    files=files,
                    descriptions=descriptions,
                    captions=captions,
                    is_thumbnails=is_thumbnails,
                    db_session=db_session,
                )
                return {"message": "Media uploaded successfully"}
            except Exception as e:
                raise CustomException(str(e))
