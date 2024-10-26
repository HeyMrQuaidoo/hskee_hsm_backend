import uuid
import pytz
from typing import Optional, List
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import event, ForeignKey, DateTime, UUID, String, Text, Boolean

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.common.enums.common_enums import PriorityEnum
from app.modules.common.models.model_base_collection import BaseModelCollection
from app.modules.communication.enums.communication_enums import MaintenanceStatusEnum


class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"
    MNT_REQ_PREFIX = "TSK"

    maintenance_request_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        # unique=True, // No need for them
        # index=True,
        default=uuid.uuid4,
    )
    task_number: Mapped[str] = mapped_column(String(128), unique=True, nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String, default=MaintenanceStatusEnum.pending, nullable=True
    )
    priority: Mapped[str] = mapped_column(
        String, default=PriorityEnum.medium, nullable=True
    )
    requested_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )
    property_unit_assoc_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("property_unit_assoc.property_unit_assoc_id"),
        nullable=True,
    )
    scheduled_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    completed_date: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc), nullable=True
    )
    is_emergency: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)

   # Foreign key to CalendarEvent
    calendar_event_id: Mapped[Optional[uuid.UUID]] = mapped_column(
        UUID(as_uuid=True), ForeignKey("calendar_events.calendar_event_id"), nullable=True
    )
    # property
    property: Mapped["Property"] = relationship(
        "Property",
        secondary="property_unit_assoc",
        primaryjoin="MaintenanceRequest.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        secondaryjoin="Property.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        viewonly=True,
        back_populates="maintenance_requests",
        lazy="selectin",
    )

    # unit
    unit: Mapped["Units"] = relationship(
        "Units",
        secondary="property_unit_assoc",
        primaryjoin="MaintenanceRequest.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        secondaryjoin="Units.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        viewonly=True,
        back_populates="maintenance_requests",
        lazy="selectin",
    )

    # property_association
    property_unit_assoc: Mapped["PropertyUnitAssoc"] = relationship(
        "PropertyUnitAssoc",
        back_populates="prop_maintenance_requests",
        cascade="save-update, merge",
        primaryjoin="MaintenanceRequest.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        # overlaps="maintenance_requests, property, unit",
        foreign_keys=[property_unit_assoc_id],
        lazy="selectin",
        viewonly=True,
    )

    # user
    user: Mapped["User"] = relationship(
        "User", back_populates="maintenance_requests", lazy="selectin"
    )


    # CalendarEvent
    calendar_event: Mapped[Optional["CalendarEvent"]] = relationship(
        "CalendarEvent",
        back_populates="maintenance_requests",
        uselist=False,
        lazy="selectin",
        cascade="all",
        single_parent=True,
        collection_class=BaseModelCollection,
    )

    # media
    media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary="entity_media",
        primaryjoin="and_(MaintenanceRequest.maintenance_request_id == EntityMedia.entity_id, EntityMedia.entity_type == 'maintenancerequests')",
        secondaryjoin="EntityMedia.media_id == Media.media_id",
        viewonly=True,
        lazy="selectin",
        collection_class=BaseModelCollection,
    )


@event.listens_for(MaintenanceRequest, "before_insert")
def receive_before_insert(mapper, connection, target: MaintenanceRequest):
    if not target.task_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.task_number = f"{MaintenanceRequest.MNT_REQ_PREFIX}{current_time_str}"


@event.listens_for(MaintenanceRequest, "after_insert")
def receive_after_insert(mapper, connection, target: MaintenanceRequest):
    if not target.task_number:
        current_time_str = datetime.now().strftime("%Y%m%d%H%M%S")
        target.task_number = f"{MaintenanceRequest.MNT_REQ_PREFIX}{current_time_str}"
        connection.execute(
            target.__table__.update()
            .where(target.__table__.c.id == target.id)
            .values(task_number=target.task_number)
        )


def parse_dates(mapper, connection, target):
    """Listener to convert date_paid and date_to to a datetime if it's provided as a string."""
    if isinstance(target.scheduled_date, str):
        # Try to convert 'scheduled_date' string to datetime with or without microseconds
        try:
            target.scheduled_date = datetime.strptime(
                target.scheduled_date, "%Y-%m-%d %H:%M:%S.%f"
            )
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.scheduled_date = datetime.strptime(target.scheduled_date, "%Y-%m-%d %H:%M:%S")

    if isinstance(target.completed_date, str):
        # Try to convert 'completed_date' string to datetime with or without microseconds
        try:
            target.completed_date = datetime.strptime(target.completed_date, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.completed_date = datetime.strptime(target.completed_date, "%Y-%m-%d %H:%M:%S")


event.listen(MaintenanceRequest, "before_insert", parse_dates)
event.listen(MaintenanceRequest, "before_update", parse_dates)

# Register model outside the class definition
Base.setup_model_dynamic_listener("maintenance_requests", MaintenanceRequest)
