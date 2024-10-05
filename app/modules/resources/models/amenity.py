import uuid
from typing import List
from sqlalchemy import String, Text, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class Amenities(Base):
    __tablename__ = "amenities"

    amenity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    amenity_name: Mapped[str] = mapped_column(String(128))
    amenity_short_name: Mapped[str] = mapped_column(String(80))
    description: Mapped[str] = mapped_column(Text)

    media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary="entity_media",
        primaryjoin="Amenities.amenity_id == EntityMedia.entity_id",
        secondaryjoin="and_(EntityMedia.media_id == Media.media_id, EntityMedia.entity_type == 'Amenities')",
        overlaps="entity_media, media",
        lazy="selectin",
    )
