# app/modules/maintenance/router/maintenance_request_router.py

from typing import List
from uuid import UUID
from fastapi import Depends, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.communication.dao.maintenance_request_dao import MaintenanceRequestDAO

# Base CRUD Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import MaintenanceRequestSchema
from app.modules.communication.schema.maintenance_request_schema import (
    MaintenanceRequestCreateSchema,
    MaintenanceRequestUpdateSchema,
    MaintenanceRequestResponse,
)

# Core
from app.core.lifespan import get_db
from app.core.errors import CustomException

class MaintenanceRequestRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: MaintenanceRequestDAO = MaintenanceRequestDAO(excludes=[])
        MaintenanceRequestSchema["create_schema"] = MaintenanceRequestCreateSchema
        MaintenanceRequestSchema["update_schema"] = MaintenanceRequestUpdateSchema
        MaintenanceRequestSchema["response_schema"] = MaintenanceRequestResponse

        super().__init__(
            dao=self.dao, schemas=MaintenanceRequestSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        @self.router.post(
            "/{id}/upload_media", status_code=status.HTTP_201_CREATED
        )
        async def upload_media_to_request(
            id: UUID,
            files: List[UploadFile] = File(...),
            descriptions: List[str] = Form(None),
            captions: List[str] = Form(None),
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                await self.dao.upload_request_media(
                    db_session=db_session,
                    request_id=str(id),
                    files=files,
                    descriptions=descriptions,
                    captions=captions,
                )
                return {"message": "Media uploaded successfully"}
            except Exception as e:
                raise CustomException(str(e))
