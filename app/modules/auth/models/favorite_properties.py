import uuid
from sqlalchemy import UUID, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


# TODO: Double check needed primary keys
class FavoriteProperties(Base):
    __tablename__ = "favorite_properties"

    favorite_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        primary_key=True,
    )
    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
        primary_key=True,
    )

    # users
    users: Mapped["User"] = relationship("User", back_populates="favorites")
