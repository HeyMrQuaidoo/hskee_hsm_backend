# app/modules/resources/models/media.py

import uuid
from typing import Optional, List
from sqlalchemy import Enum, String, UUID, Boolean, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Base model
from app.modules.common.models.model_base import BaseModel as Base

# Enums
from app.modules.resources.enums.resource_enums import MediaType


class Media(Base):
    __tablename__ = "media"

    media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    content_url: Mapped[str] = mapped_column(Text)
    media_name: Mapped[str] = mapped_column(String(128))
    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType), default=MediaType.other
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    caption: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_thumbnail: Mapped[bool] = mapped_column(Boolean, default=False)

    # Relationships
    entity_media: Mapped[List["EntityMedia"]] = relationship(
        "EntityMedia",
        back_populates="media",
        lazy="selectin",
    )
