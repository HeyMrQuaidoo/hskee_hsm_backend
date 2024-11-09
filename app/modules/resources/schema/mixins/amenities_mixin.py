from uuid import UUID
from typing import Optional

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.common.schema.base_schema import BaseSchema


class AmenityBase(BaseSchema):
    amenity_id: Optional[UUID] = None
    amenity_name: Optional[str] = None
    amenity_short_name: Optional[str] = None
    description: Optional[str] = None


class Amenity(AmenityBase):
    amenity_id: Optional[UUID]


class AmenityInfoMixin:
    _amenity_name = BaseFaker.word()
    _amenity_short_name = BaseFaker.word()
    _description = BaseFaker.sentence()

    _amenity_create_json = {
        "amenity_name": _amenity_name,
        "amenity_short_name": _amenity_short_name,
        "description": _description,
    }

    _amenity_update_json = {
        "amenity_name": _amenity_name,
        "amenity_short_name": _amenity_short_name,
        "description": _description,
    }
