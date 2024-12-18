# app/modules/maintenance/router/maintenance_request_router.py

from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import Depends, Query, status, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.core.response import DAOResponse
from app.modules.common.enums.common_enums import PriorityEnum
from app.modules.communication.dao.maintenance_request_dao import MaintenanceRequestDAO

# Base CRUD Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import MaintenanceRequestSchema
from app.modules.communication.enums.communication_enums import MaintenanceStatusEnum
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
        @self.router.get("/")
        async def get_requests(
            user_id: Optional[UUID] = Query(None),
            status: Optional[MaintenanceStatusEnum] = Query(None),
            priority: Optional[PriorityEnum] = Query(None),
            task_number: Optional[str] = Query(None),
            scheduled_date_gte: Optional[datetime] = Query(None),
            scheduled_date_lte: Optional[datetime] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_requests(
                db_session=db_session,
                user_id=user_id,
                status=status,
                priority=priority,
                task_number=task_number,
                scheduled_date_gte=scheduled_date_gte,
                scheduled_date_lte=scheduled_date_lte,
                limit=limit,
                offset=offset,
            )

        @self.router.post("/{id}/upload_media", status_code=status.HTTP_201_CREATED)
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
