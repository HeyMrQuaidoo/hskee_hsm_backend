# app/modules/communication/dao/calendar_event_dao.py

from typing import Optional, List

# Base DAO
from app.modules.common.dao.base_dao import BaseDAO

# Models
from app.modules.communication.models.calendar_event import CalendarEvent


class CalendarEventDAO(BaseDAO[CalendarEvent]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = CalendarEvent

        # Detail mappings for creating related entities
        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="calendar_event_id",
        )
