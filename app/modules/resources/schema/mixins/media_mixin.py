from uuid import UUID
from typing import Annotated, Optional
from pydantic import BaseModel, ConfigDict, constr

# schema
from app.modules.common.schema.base_schema import BaseSchema


class EntityMediaCreateSchema(BaseModel):
    """
    Schema for creating an entity media association.

    Attributes:
        entity_media_id (Optional[UUID]): The unique identifier for the entity media association.
        entity_type (str): The type of the entity.
        media_id (UUID): The unique identifier for the media.
        media_assoc_id (UUID): The unique identifier for the media association.
    """

    entity_media_id: Optional[UUID] = None
    entity_type: Annotated[str, constr(max_length=50)]
    media_id: UUID
    media_assoc_id: UUID

    model_config = ConfigDict(from_attributes=True)


class MediaBase(BaseSchema):
    media_name: str
    media_type: str = None
    content_url: str = None
    is_thumbnail: Optional[bool] = None
    caption: Optional[str] = None
    description: Optional[str] = None


class Media(MediaBase):
    media_id: Optional[UUID]
