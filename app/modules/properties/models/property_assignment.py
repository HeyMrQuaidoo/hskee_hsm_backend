import uuid
import pytz
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import ForeignKey, DateTime, Enum, Text, UUID

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
    property_unit_assoc: Mapped["PropertyUnitAssoc"] = relationship(
        "PropertyUnitAssoc", lazy="selectin", viewonly=True
    )

    # users
    user: Mapped["User"] = relationship("User", lazy="selectin", viewonly=True)
