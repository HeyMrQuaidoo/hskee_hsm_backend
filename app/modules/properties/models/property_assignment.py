from typing import List
import uuid
import pytz
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Enum, Text, UUID, event

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.properties.enums.property_enums import PropertyAssignmentType


class PropertyAssignment(Base):
    __tablename__ = "property_assignment"

    property_assignment_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_unit_assoc.property_unit_assoc_id")
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    assignment_type: Mapped[PropertyAssignmentType] = mapped_column(
        Enum(PropertyAssignmentType)
    )
    date_from: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    date_to: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    notes: Mapped[str] = mapped_column(Text)

    # property_association
    property_info: Mapped["PropertyUnitAssoc"] = relationship(
        "PropertyUnitAssoc", lazy="selectin", viewonly=True
    )

    # property
    property: Mapped[List["Property"]] = relationship(
        "Property",
        primaryjoin="and_(Property.property_unit_assoc_id == PropertyAssignment.property_unit_assoc_id)",
        # back_populates="property_assignment",
        foreign_keys="[PropertyAssignment.property_unit_assoc_id]",
        remote_side="[Property.property_unit_assoc_id]",
        lazy="selectin",
        viewonly=True,
    )

    # users
    user: Mapped["User"] = relationship(
        "User",
        foreign_keys="[PropertyAssignment.user_id]",
        back_populates="property_assignment",
        lazy="selectin",
        viewonly=True,
    )


def parse_dates(mapper, connection, target):
    """Listener to convert date_from and date_to to a datetime if it's provided as a string."""
    if isinstance(target.date_from, str):
        # Try to convert 'date_from' string to datetime with or without microseconds
        try:
            target.date_from = datetime.strptime(
                target.date_from, "%Y-%m-%d %H:%M:%S.%f"
            )
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.date_from = datetime.strptime(target.date_from, "%Y-%m-%d %H:%M:%S")

    if isinstance(target.date_to, str):
        # Try to convert 'date_to' string to datetime with or without microseconds
        try:
            target.date_to = datetime.strptime(target.date_to, "%Y-%m-%d %H:%M:%S.%f")
        except ValueError:
            # Fallback to parsing without microseconds if not present
            target.date_to = datetime.strptime(target.date_to, "%Y-%m-%d %H:%M:%S")


event.listen(PropertyAssignment, "before_insert", parse_dates)
event.listen(PropertyAssignment, "before_update", parse_dates)

# register model
Base.setup_model_dynamic_listener("property_assignment", PropertyAssignment)
