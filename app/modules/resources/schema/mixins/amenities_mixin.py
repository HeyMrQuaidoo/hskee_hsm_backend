from uuid import UUID
from typing import Optional

# schema
from app.modules.common.schema.base_schema import BaseSchema


class AmenityBase(BaseSchema):
    amenity_name: Optional[str] = None
    amenity_short_name: Optional[str] = None
    description: Optional[str] = None


class Amenity(AmenityBase):
    amenity_id: Optional[UUID]
