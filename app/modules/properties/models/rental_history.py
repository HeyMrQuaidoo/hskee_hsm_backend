import uuid
from typing import List
from datetime import datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import DateTime, UUID, String, ForeignKey, event

# models
from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


class PastRentalHistory(Base):
    __tablename__ = "past_rental_history"

    rental_history_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    start_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    property_owner_name: Mapped[str] = mapped_column(String, nullable=False)
    property_owner_email: Mapped[str] = mapped_column(String, nullable=False)
    property_owner_mobile: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=False
    )

    # users
    user: Mapped["User"] = relationship("User", back_populates="rental_history")

    # addresses
    address: Mapped[List["Addresses"]] = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(PastRentalHistory.rental_history_id==EntityAddress.entity_id, EntityAddress.entity_type=='pastrentalhistory')",
        secondaryjoin="EntityAddress.address_id==Addresses.address_id",
        # overlaps="address,entity_addresses,addresses,properties,users",
        back_populates="rental_history",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )


def sanitize_datetime(mapper, connection, target):
    """Listener to convert date_of_birth to a date if it's provided as a string."""
    if isinstance(target.start_date, str):
        # (format 'YYYY-MM-DD')
        target.start_date = datetime.strptime(
            target.start_date, "%Y-%m-%d %H:%M:%S"
        ).date()

    if isinstance(target.end_date, str):
        # (format 'YYYY-MM-DD')
        target.end_date = datetime.strptime(target.end_date, "%Y-%m-%d %H:%M:%S").date()


event.listen(PastRentalHistory, "before_insert", sanitize_datetime)
event.listen(PastRentalHistory, "before_update", sanitize_datetime)

# register model
Base.setup_model_dynamic_listener("past_rental_history", PastRentalHistory)
