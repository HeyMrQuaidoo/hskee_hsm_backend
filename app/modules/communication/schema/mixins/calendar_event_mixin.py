from uuid import UUID
from typing import Optional, List
from datetime import datetime

# Enums
from app.modules.communication.enums.communication_enums import (
    CalendarStatusEnum,
    EventTypeEnum,
)

# Base schema
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema

# Models
from app.modules.communication.models.calendar_event import (
    CalendarEvent as CalendarEventModel,
)
from app.modules.auth.schema.mixins.user_mixin import UserBaseMixin

class CalendarEventBase(BaseSchema):
    title: str
    description: Optional[str] = None
    status: CalendarStatusEnum
    event_type: EventTypeEnum
    event_start_date: Optional[datetime] = None
    event_end_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    organizer_id: UUID

class CalendarEventInfoMixin(UserBaseMixin):
    # Faker attributes
    _title = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)
    _status = BaseFaker.random_element([e.value for e in CalendarStatusEnum])
    _event_type = BaseFaker.random_element([e.value for e in EventTypeEnum])
    _event_start_date = BaseFaker.future_datetime()
    _event_end_date = BaseFaker.future_datetime()
    _completed_date = BaseFaker.future_datetime()
    _organizer_id = str(BaseFaker.uuid4())

    _calendar_event_create_json = {
        "title": _title,
        "description": _description,
        "status": _status,
        "event_type": _event_type,
        "event_start_date": _event_start_date.isoformat(),
        "event_end_date": _event_end_date.isoformat(),
        "completed_date": _completed_date.isoformat(),
        "organizer_id": _organizer_id,
    }

    _calendar_event_update_json = {
        "title": _title,
        "description": _description,
        "status": _status,
        "event_type": _event_type,
        "event_start_date": _event_start_date.isoformat(),
        "event_end_date": _event_end_date.isoformat(),
        "completed_date": _completed_date.isoformat(),
    }

    @classmethod
    def model_validate(cls, calendar_event: CalendarEventModel):
        return cls(
            calendar_event_id=calendar_event.calendar_event_id,
            event_id=calendar_event.event_id,
            title=calendar_event.title,
            description=calendar_event.description,
            status=calendar_event.status,
            event_type=calendar_event.event_type,
            event_start_date=calendar_event.event_start_date,
            event_end_date=calendar_event.event_end_date,
            completed_date=calendar_event.completed_date,
            organizer_id=calendar_event.organizer_id,
            organizer=cls.get_user_info(calendar_event.organizer),
        )
