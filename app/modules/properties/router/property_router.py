from typing import List, Optional
from pydantic import UUID4
from fastapi import Depends, Query, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

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

# Enums
from app.modules.properties.enums.property_enums import PropertyType, PropertyStatus

# Core
from app.core.lifespan import get_db
from app.core.response import DAOResponse
from app.core.errors import CustomException


class PropertyRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: PropertyDAO = PropertyDAO(excludes=[])
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        PropertySchema["response_schema"] = PropertyResponse

        super().__init__(
            dao=self.dao,
            schemas=PropertySchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/")
        async def get_all_properties(
            name: Optional[str] = Query(None),
            property_type: Optional[PropertyType] = Query(None),
            amount_gte: Optional[float] = Query(None),
            amount_lte: Optional[float] = Query(None),
            floor_space_gte: Optional[float] = Query(None),
            floor_space_lte: Optional[float] = Query(None),
            num_units: Optional[int] = Query(None),
            num_bathrooms: Optional[int] = Query(None),
            num_garages: Optional[int] = Query(None),
            has_balconies: Optional[bool] = Query(None),
            has_parking_space: Optional[bool] = Query(None),
            pets_allowed: Optional[bool] = Query(None),
            property_status: Optional[PropertyStatus] = Query(None),
            is_contract_active: Optional[bool] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_properties(
                db_session=db_session,
                name=name,
                property_type=property_type,
                amount_gte=amount_gte,
                amount_lte=amount_lte,
                floor_space_gte=floor_space_gte,
                floor_space_lte=floor_space_lte,
                num_units=num_units,
                num_bathrooms=num_bathrooms,
                num_garages=num_garages,
                has_balconies=has_balconies,
                has_parking_space=has_parking_space,
                pets_allowed=pets_allowed,
                property_status=property_status,
                is_contract_active=is_contract_active,
                limit=limit,
                offset=offset,
            )

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
