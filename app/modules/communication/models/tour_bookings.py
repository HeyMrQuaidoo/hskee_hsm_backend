import uuid
import pytz
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import UUID, String, Enum, DateTime, ForeignKey

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.communication.enums.communication_enums import TourStatus, TourType


class TourBookings(Base):
    __tablename__ = "tour"

    tour_booking_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        index=True,
        default=uuid.uuid4,
    )
    name: Mapped[str] = mapped_column(String)
    email: Mapped[str] = mapped_column(String)
    phone_number: Mapped[str] = mapped_column(String)
    tour_type: Mapped[TourType] = mapped_column(
        Enum(TourType), default=TourType.in_person, nullable=True, name="tour_type"
    )
    status: Mapped[TourStatus] = mapped_column(
        Enum(TourStatus),
        default=TourStatus.incoming,
        nullable=True,
        name="status",
    )
    tour_date: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=True,
    )

    # user
    user: Mapped["User"] = relationship("User", back_populates="tours", lazy="selectin")

    # property
    property: Mapped["Property"] = relationship(
        "Property",
        secondary="property_unit_assoc",
        primaryjoin="TourBookings.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        secondaryjoin="Property.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        viewonly=True,
        back_populates="tour_bookings",
        lazy="selectin",
    )

    # unit
    unit: Mapped["Units"] = relationship(
        "Units",
        secondary="property_unit_assoc",
        primaryjoin="TourBookings.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        secondaryjoin="Units.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        viewonly=True,
        back_populates="tour_bookings",
        lazy="selectin",
    )

    # property_association
    property_unit_assoc: Mapped["PropertyUnitAssoc"] = relationship(
        "PropertyUnitAssoc",
        back_populates="prop_unit_assoc_tours",
        cascade="save-update, merge",
        primaryjoin="TourBookings.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
        overlaps="property,unit",
        foreign_keys=[property_unit_assoc_id],
        lazy="selectin",
        viewonly=True,
    )
