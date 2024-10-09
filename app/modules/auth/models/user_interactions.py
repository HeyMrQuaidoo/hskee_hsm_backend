import pytz
import uuid
from datetime import datetime
from sqlalchemy import DateTime, ForeignKey, Text, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class UserInteractions(Base):
    __tablename__ = "user_interactions"

    user_interaction_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )
    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_unit_assoc.property_unit_assoc_id")
    )
    contact_time: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(pytz.utc)
    )
    contact_details: Mapped[str] = mapped_column(Text)

    # users
    user: Mapped["User"] = relationship(
        "User", foreign_keys=[user_id], back_populates="interactions_as_user"
    )
    employee: Mapped["User"] = relationship(
        "User", foreign_keys=[employee_id], back_populates="interactions_as_employee"
    )
