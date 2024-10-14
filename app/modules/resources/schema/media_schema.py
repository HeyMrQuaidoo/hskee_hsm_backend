from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import ConfigDict

# Schema mixin
from app.modules.resources.schema.mixins.media_mixin import MediaBase

# Base Faker
from app.modules.common.schema.base_schema import BaseFaker

# Models
from app.modules.resources.models.media import Media as MediaModel


class MediaCreateSchema(MediaBase):
    # Faker attributes
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_choices(
        ["image", "video", "audio", "document"], length=1
    )
    _content_url = BaseFaker.url()
    _is_thumbnail = BaseFaker.boolean()
    _caption = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "media_name": _media_name,
                "media_type": _media_type[0],
                "content_url": _content_url,
                "is_thumbnail": _is_thumbnail,
                "caption": _caption,
                "description": _description,
            }
        },
    )


class MediaUpdateSchema(MediaBase):
    # Faker attributes
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_choices(
        ["image", "video", "audio", "document"], length=1
    )
    _content_url = BaseFaker.url()
    _is_thumbnail = BaseFaker.boolean()
    _caption = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "media_name": _media_name,
                "media_type": _media_type[0],
                "content_url": _content_url,
                "is_thumbnail": _is_thumbnail,
                "caption": _caption,
                "description": _description,
            }
        },
    )


class MediaResponse(MediaBase):
    media_id: Optional[UUID] = None

    @classmethod
    def model_validate(cls, media: MediaModel) -> "MediaResponse":
        return cls(
            media_id=media.media_id,
            media_name=media.media_name,
            media_type=media.media_type,
            content_url=media.content_url,
            is_thumbnail=media.is_thumbnail,
            caption=media.caption,
            description=media.description,
        ).model_dump()
