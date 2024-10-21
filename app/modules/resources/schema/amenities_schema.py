from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import ConfigDict

# schemas
from app.modules.resources.schema.mixins.amenities_mixin import (
    AmenityBase,
    AmenityInfoMixin,
)

# models
from app.modules.resources.models.amenity import Amenities as AmenitiesModel


class AmenityCreateSchema(AmenityBase, AmenityInfoMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": AmenityInfoMixin._amenity_create_json},
    )


class AmenityUpdateSchema(AmenityBase):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": AmenityInfoMixin._amenity_update_json},
    )


class AmenityResponse(AmenityBase):
    amenity_id: Optional[UUID] = None

    @classmethod
    def model_validate(cls, amenity: AmenitiesModel) -> "AmenityResponse":
        return cls(
            amenity_id=amenity.amenity_id,
            amenity_name=amenity.amenity_name,
            amenity_short_name=amenity.amenity_short_name,
            description=amenity.description,
        ).model_dump()
