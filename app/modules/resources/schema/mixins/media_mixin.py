from uuid import UUID
from typing import Annotated, Optional
from pydantic import ConfigDict, constr

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.resources.enums.resource_enums import MediaType


class EntityMediaCreateSchema(BaseSchema):
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
    media_name: Optional[str] = None
    media_type: Optional[MediaType] = None
    content_url: Optional[str] = None
    is_thumbnail: Optional[bool] = False
    caption: Optional[str] = None
    description: Optional[str] = None


class Media(MediaBase):
    media_id: Optional[UUID]


class MediaInfoMixin:
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_choices(
        ["image", "video", "audio", "document"], length=1
    )
    _content_url = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAApgAAAKYB3X3/OAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBlLm9yZ5vuPBoAAANCSURBVEiJtZZPbBtFFMZ/M7ubXdtdb1xSFyeilBapySVU8h8OoFaooFSqiihIVIpQBKci6KEg9Q6H9kovIHoCIVQJJCKE1ENFjnAgcaSGC6rEnxBwA04Tx43t2FnvDAfjkNibxgHxnWb2e/u992bee7tCa00YFsffekFY+nUzFtjW0LrvjRXrCDIAaPLlW0nHL0SsZtVoaF98mLrx3pdhOqLtYPHChahZcYYO7KvPFxvRl5XPp1sN3adWiD1ZAqD6XYK1b/dvE5IWryTt2udLFedwc1+9kLp+vbbpoDh+6TklxBeAi9TL0taeWpdmZzQDry0AcO+jQ12RyohqqoYoo8RDwJrU+qXkjWtfi8Xxt58BdQuwQs9qC/afLwCw8tnQbqYAPsgxE1S6F3EAIXux2oQFKm0ihMsOF71dHYx+f3NND68ghCu1YIoePPQN1pGRABkJ6Bus96CutRZMydTl+TvuiRW1m3n0eDl0vRPcEysqdXn+jsQPsrHMquGeXEaY4Yk4wxWcY5V/9scqOMOVUFthatyTy8QyqwZ+kDURKoMWxNKr2EeqVKcTNOajqKoBgOE28U4tdQl5p5bwCw7BWquaZSzAPlwjlithJtp3pTImSqQRrb2Z8PHGigD4RZuNX6JYj6wj7O4TFLbCO/Mn/m8R+h6rYSUb3ekokRY6f/YukArN979jcW+V/S8g0eT/N3VN3kTqWbQ428m9/8k0P/1aIhF36PccEl6EhOcAUCrXKZXXWS3XKd2vc/TRBG9O5ELC17MmWubD2nKhUKZa26Ba2+D3P+4/MNCFwg59oWVeYhkzgN/JDR8deKBoD7Y+ljEjGZ0sosXVTvbc6RHirr2reNy1OXd6pJsQ+gqjk8VWFYmHrwBzW/n+uMPFiRwHB2I7ih8ciHFxIkd/3Omk5tCDV1t+2nNu5sxxpDFNx+huNhVT3/zMDz8usXC3ddaHBj1GHj/As08fwTS7Kt1HBTmyN29vdwAw+/wbwLVOJ3uAD1wi/dUH7Qei66PfyuRj4Ik9is+hglfbkbfR3cnZm7chlUWLdwmprtCohX4HUtlOcQjLYCu+fzGJH2QRKvP3UNz8bWk1qMxjGTOMThZ3kvgLI5AzFfo379UAAAAASUVORK5CYII="
    _is_thumbnail = BaseFaker.boolean()
    _caption = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)

    _media_create_json = {
        "media_name": _media_name,
        "media_type": _media_type[0],
        "content_url": _content_url,
        "is_thumbnail": _is_thumbnail,
        "caption": _caption,
        "description": _description,
    }

    _media_update_json = {
        "media_name": _media_name,
        "media_type": _media_type[0],
        "content_url": _content_url,
        "is_thumbnail": _is_thumbnail,
        "caption": _caption,
        "description": _description,
    }
