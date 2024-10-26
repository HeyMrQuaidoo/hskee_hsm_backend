import uuid
import pytz
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import event, ForeignKey, DateTime, Enum, UUID, String, Text

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.communication.enums.communication_enums import (
    CalendarStatusEnum,
    EventTypeEnum,
)


class CalendarEvent(Base):
    __tablename__ = "calendar_events"
    CAL_EVENT_PREFIX = "EV"

    calendar_event_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        # unique=True, // No need for them
        # index=True,
        default=uuid.uuid4,
    )
    event_id: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[CalendarStatusEnum] = mapped_column(
        Enum(CalendarStatusEnum), default=CalendarStatusEnum.pending
    )
    event_type: Mapped[EventTypeEnum] = mapped_column(
        Enum(EventTypeEnum), default=EventTypeEnum.other, nullable=True
    )
    event_start_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    event_end_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    completed_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    organizer_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    # users
    organizer: Mapped["User"] = relationship(
        "User", back_populates="events", lazy="selectin"
    )

    # Relationship to MaintenanceRequest
    maintenance_requests: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest",
        back_populates="calendar_event",
        lazy="selectin",
    )


@event.listens_for(CalendarEvent, "before_insert")
def receive_before_insert(mapper, connection, target: CalendarEvent):
    if not target.event_id:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.event_id = f"{CalendarEvent.CAL_EVENT_PREFIX}{current_time_str}"


@event.listens_for(CalendarEvent, "after_insert")
def receive_after_insert(mapper, connection, target: CalendarEvent):
    if not target.event_id:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.event_id = f"{CalendarEvent.CAL_EVENT_PREFIX}{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(event_id=target.event_id)
        )

def parse_dates(mapper, connection, target):
    """Listener to convert date_paid and date_to to a datetime if it's provided as a string."""
    if isinstance(target.event_start_date, str):
        # Try to convert 'event_start_date' string to datetime with or without microseconds
        try:
            target.event_start_date = datetime.strptime(
                target.event_start_date, "%Y-%m-%d %H:%M:%S.%f"
            )
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.event_start_date = datetime.strptime(target.event_start_date, "%Y-%m-%d %H:%M:%S")

    if isinstance(target.event_end_date, str):
        # Try to convert 'event_end_date' string to datetime with or without microseconds
        try:
            target.event_end_date = datetime.strptime(target.event_end_date, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.event_end_date = datetime.strptime(target.event_end_date, "%Y-%m-%d %H:%M:%S")

    if isinstance(target.completed_date, str):
        # Try to convert 'completed_date' string to datetime with or without microseconds
        try:
            target.completed_date = datetime.strptime(target.completed_date, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.completed_date = datetime.strptime(target.completed_date, "%Y-%m-%d %H:%M:%S")


event.listen(CalendarEvent, "before_insert", parse_dates)
event.listen(CalendarEvent, "before_update", parse_dates)

# Register model outside the class definition
Base.setup_model_dynamic_listener("calendar_events", CalendarEvent)
