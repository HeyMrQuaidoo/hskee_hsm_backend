from datetime import date
from pydantic import ConfigDict
from typing import Any, Optional, Union

# schema
from app.modules.address.schema.address_mixin import AddressMixin
from app.modules.properties.schema.mixins.property_mixin import (
    PropertyInfoMixin,
    PropertyBase,
)

# models
from app.modules.properties.models.property import Property as PropertyModel


class PropertyResponse(PropertyBase, PropertyInfoMixin):
    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property)


class PropertyCreateSchema(PropertyBase, PropertyInfoMixin, AddressMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": PropertyInfoMixin._property_create_json},
    )

    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property)


class PropertyUpdateSchema(PropertyBase, PropertyInfoMixin, AddressMixin):
    name: Optional[str] = None
    property_type: Union[Any] = None
    amount: float = None
    property_status: Union[Any] = None
    security_deposit: Optional[float] = None
    commission: Optional[float] = None
    floor_space: Optional[float] = None
    num_units: Optional[int] = None
    num_bathrooms: Optional[int] = None
    num_garages: Optional[int] = None
    has_balconies: Optional[bool] = False
    has_parking_space: Optional[bool] = False
    pets_allowed: bool = False
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": PropertyInfoMixin._property_update_json},
    )

    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property)
