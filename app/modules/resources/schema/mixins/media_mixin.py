from uuid import UUID
from typing import Optional

# schema
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.resources.enums.resource_enums import MediaType


class MediaBase(BaseSchema):
    media_name: Optional[str] = None
    media_type: Optional[MediaType] = None
    content_url: Optional[str] = None
    is_thumbnail: Optional[bool] = False
    caption: Optional[str] = None
    description: Optional[str] = None


class Media(MediaBase):
    media_id: Optional[UUID]
