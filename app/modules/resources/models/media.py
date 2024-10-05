import uuid
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum, String, UUID, Boolean, Text

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.resources.enums.resource_enums import MediaType


class Media(Base):
    __tablename__ = "media"

    media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    content_url: Mapped[str] = mapped_column(Text)
    media_name: Mapped[str] = mapped_column(String(128))
    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType), default=MediaType.other
    )
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    caption: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    is_thumbnail: Mapped[bool] = mapped_column(Boolean, default=False)
