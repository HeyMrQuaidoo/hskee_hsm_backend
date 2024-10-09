from pydantic import BaseModel, UUID4
from typing import Optional

class MediaBase(BaseModel):
    content_url: str
    media_name: str
    media_type: str
    description: Optional[str] = None
    caption: Optional[str] = None
    is_thumbnail: Optional[bool] = False

class MediaCreateSchema(MediaBase):
    pass

class MediaUpdateSchema(MediaBase):
    pass

class MediaSchema(MediaBase):
    media_id: UUID4
