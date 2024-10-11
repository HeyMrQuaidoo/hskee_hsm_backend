from uuid import UUID
from datetime import date
from typing import Optional
from pydantic import ConfigDict

# Base Faker
from app.modules.common.schema.base_schema import BaseFaker

# Models
from app.modules.resources.models.amenity import Amenities as AmenitiesModel

class AmenityBase(BaseModel):
    amenity_name: Optional[str] = None
    amenity_short_name: Optional[str] = None
    description: Optional[str] = None

class AmenityCreateSchema(AmenityBase):
    # Faker attributes
    _amenity_name = BaseFaker.word()
    _amenity_short_name = BaseFaker.word()
    _description = BaseFaker.sentence()

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "amenity_name": _amenity_name,
                "amenity_short_name": _amenity_short_name,
                "description": _description,
            }
        },
    )

class AmenityUpdateSchema(AmenityBase):
    # Faker attributes
    _amenity_name = BaseFaker.word()
    _amenity_short_name = BaseFaker.word()
    _description = BaseFaker.sentence()

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "amenity_name": _amenity_name,
                "amenity_short_name": _amenity_short_name,
                "description": _description,
            }
        },
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
