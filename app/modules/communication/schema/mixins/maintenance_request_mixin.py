from uuid import UUID
from typing import List, Optional
from datetime import datetime

# Enums
from app.modules.communication.enums.communication_enums import EventTypeEnum, MaintenanceStatusEnum
from app.modules.common.enums.common_enums import PriorityEnum

# Base schema
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema

# Models
from app.modules.communication.models.maintenance_requests import (
    MaintenanceRequest as MaintenanceRequestModel,
)

# Mixins
from app.modules.auth.schema.mixins.user_mixin import UserBaseMixin
from app.modules.communication.schema.mixins.calendar_event_mixin import CalendarEventBase, CalendarEventInfoMixin
from app.modules.resources.schema.media_schema import MediaBase 


class MaintenanceRequestBase(BaseSchema):
    title: str
    description: Optional[str] = None
    status: MaintenanceStatusEnum
    priority: PriorityEnum
    requested_by: UUID
    property_unit_assoc_id: Optional[UUID] = None
    scheduled_date: Optional[datetime] = None
    completed_date: Optional[datetime] = None
    is_emergency: bool
    calendar_event: Optional[CalendarEventBase] = None
    media: Optional[List[MediaBase]] = None

class MaintenanceRequestInfoMixin(UserBaseMixin):
    # Faker attributes
    _title = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)
    _status = BaseFaker.random_element([e.value for e in MaintenanceStatusEnum])
    _priority = BaseFaker.random_element([e.value for e in PriorityEnum])
    _requested_by = "c5087963-8653-406d-b6c3-f16150e7ee21"
    _property_unit_assoc_id = "2e3b1dfc-2a75-4311-b27b-bc4f5b208db5"
    _scheduled_date = BaseFaker.future_datetime()
    _completed_date = BaseFaker.future_datetime()
    _is_emergency = BaseFaker.boolean()
    _event_type = BaseFaker.random_element([e.value for e in EventTypeEnum])
    _event_start_date = BaseFaker.future_datetime()
    _event_end_date = BaseFaker.future_datetime()
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_choices(
        ["image", "video", "audio", "document"], length=1
    )
    _content_url = BaseFaker.url()
    _is_thumbnail = BaseFaker.boolean()
    _caption = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)


     # Faker attributes for calendar_event
    _calendar_event = {
        "title": _title,
        "description": _description,
        "status": "pending",
        "event_type": _event_type,
        "event_start_date": _scheduled_date.isoformat(),
        "event_end_date": _event_end_date.isoformat(),
        "completed_date": _completed_date.isoformat(),
        "organizer_id": _requested_by,
    }

     # Faker attributes for media
    _media = [
        {
            "media_name": _media_name,
            "media_type": "image",
            "content_url": _content_url,
            "is_thumbnail": _is_thumbnail,
            "caption": _caption,
            "description": _description,
        },
        {
                "media_name": _media_name,
                "media_type": "image",
                "content_url": _content_url,
                "is_thumbnail": _is_thumbnail,
                "caption": _caption,
                "description": _description,
            },
    ]

    _maintenance_request_create_json = {
        "title": _title,
        "description": _description,
        "status": _status,
        "priority": _priority,
        "requested_by": _requested_by,
        "property_unit_assoc_id": _property_unit_assoc_id,
        "scheduled_date": _scheduled_date.isoformat(),
        "completed_date": _completed_date.isoformat(),
        "is_emergency": _is_emergency,
        "calendar_event": _calendar_event,
        "media": _media,
    }

    _maintenance_request_update_json = {
        "title": _title,
        "description": _description,
        "status": _status,
        "priority": _priority,
        "scheduled_date": _scheduled_date.isoformat(),
        "completed_date": _completed_date.isoformat(),
        "is_emergency": _is_emergency,
        "calendar_event_id": _calendar_event,
        "media": _media,
    }

    @classmethod
    def model_validate(cls, maintenance_requests: MaintenanceRequestModel):
        return cls(
            maintenance_request_id=maintenance_requests.maintenance_request_id,
            task_number=maintenance_requests.task_number,
            title=maintenance_requests.title,
            description=maintenance_requests.description,
            status=maintenance_requests.status,
            priority=maintenance_requests.priority,
            requested_by=maintenance_requests.requested_by,
            requester=cls.get_user_info(maintenance_requests.requested_by),
            property_unit_assoc_id=maintenance_requests.property_unit_assoc_id,
            scheduled_date=maintenance_requests.scheduled_date,
            completed_date=maintenance_requests.completed_date,
            is_emergency=maintenance_requests.is_emergency,
            calendar_event_id=maintenance_requests.calendar_event_id,
            calendar_event=CalendarEventBase.model_validate(
                maintenance_requests.calendar_event
            ),
            media=[
                MediaBase.model_validate(media) for media in maintenance_requests.media
            ]
        )
