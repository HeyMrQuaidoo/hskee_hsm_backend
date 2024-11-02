from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

# Enums
from app.modules.communication.enums.communication_enums import (
    CalendarStatusEnum,
    EventTypeEnum,
)

# Mixins
from app.modules.communication.models.calendar_event import CalendarEvent
from app.modules.communication.schema.mixins.calendar_event_mixin import (
    CalendarEventBase,
    CalendarEventInfoMixin,
)


class CalendarEventCreateSchema(CalendarEventBase, CalendarEventInfoMixin):
    model_config = ConfigDict(
        json_schema_extra={
            "example": CalendarEventInfoMixin._calendar_event_create_json
        },
    )


class CalendarEventUpdateSchema(CalendarEventBase, CalendarEventInfoMixin):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[CalendarStatusEnum] = None
    event_type: Optional[EventTypeEnum] = None
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": CalendarEventInfoMixin._calendar_event_update_json
        },
    )


class CalendarEventResponse(CalendarEventBase, CalendarEventInfoMixin):
    id: UUID
    event_id: str

    @classmethod
    def model_validate(cls, calendar_event: CalendarEvent):
        return super().model_validate(calendar_event)
