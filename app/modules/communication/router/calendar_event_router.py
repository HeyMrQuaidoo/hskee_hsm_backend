from typing import List
from uuid import UUID
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.communication.dao.calendar_event_dao import CalendarEventDAO

# Base CRUD Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import CalendarEventSchema
from app.modules.communication.schema.calendar_event_schema import (
    CalendarEventCreateSchema,
    CalendarEventUpdateSchema,
    CalendarEventResponse,
)

# Core
from app.core.lifespan import get_db
from app.core.errors import CustomException

class CalendarEventRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: CalendarEventDAO = CalendarEventDAO(excludes=[])
        CalendarEventSchema["create_schema"] = CalendarEventCreateSchema
        CalendarEventSchema["update_schema"] = CalendarEventUpdateSchema
        CalendarEventSchema["response_schema"] = CalendarEventResponse

        super().__init__(
            dao=self.dao, schemas=CalendarEventSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
