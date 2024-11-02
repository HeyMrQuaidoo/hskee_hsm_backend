# app/modules/maintenance/schema/maintenance_request_schema.py

from uuid import UUID
from typing import List, Optional
from datetime import datetime
from pydantic import ConfigDict

# Enums
from app.modules.communication.enums.communication_enums import MaintenanceStatusEnum
from app.modules.common.enums.common_enums import PriorityEnum

# Mixins
from app.modules.communication.schema.mixins.maintenance_request_mixin import (
    MaintenanceRequestBase,
    MaintenanceRequestInfoMixin,
)

# Schema
from app.modules.resources.schema.media_schema import MediaCreateSchema

# Models
from app.modules.communication.models.maintenance_requests import MaintenanceRequest


class MaintenanceRequestCreateSchema(
    MaintenanceRequestBase, MaintenanceRequestInfoMixin
):
    model_config = ConfigDict(
        json_schema_extra={
            "example": MaintenanceRequestInfoMixin._maintenance_request_create_json
        },
    )


class MaintenanceRequestUpdateSchema(
    MaintenanceRequestBase, MaintenanceRequestInfoMixin
):
    title: Optional[str] = None
    status: Optional[MaintenanceStatusEnum] = None
    priority: Optional[PriorityEnum] = None
    is_emergency: Optional[bool] = None
    media: Optional[List[MediaCreateSchema]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": MaintenanceRequestInfoMixin._maintenance_request_update_json
        },
    )


class MaintenanceRequestResponse(MaintenanceRequestBase, MaintenanceRequestInfoMixin):
    id: UUID
    task_number: str

    @classmethod
    def model_validate(cls, maintenance_requests: MaintenanceRequest):
        return super().model_validate(maintenance_requests)
