from datetime import date
from pydantic import ConfigDict

# schema
from app.modules.address.schema.address_mixin import AddressMixin
from app.modules.properties.schema.mixins.property_mixin import (
    PropertyUnitBase,
    PropertyUnitInfoMixin,
)

# models
from app.modules.properties.models.unit import Units as UnitModel


class UnitsResponse(PropertyUnitBase, PropertyUnitInfoMixin):
    @classmethod
    def model_validate(cls, property_unit: UnitModel):
        return cls.get_property_unit_info(property_unit).model_dump()


class UnitCreateSchema(PropertyUnitBase, PropertyUnitInfoMixin, AddressMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": PropertyUnitInfoMixin._unit_create_json},
    )

    @classmethod
    def model_validate(cls, property_unit: UnitModel):
        return cls.get_property_unit_info(property_unit).model_dump()


class UnitUpdateSchema(PropertyUnitBase, PropertyUnitInfoMixin, AddressMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={"example": PropertyUnitInfoMixin._unit_update_json},
    )

    @classmethod
    def model_validate(cls, property_unit: UnitModel):
        return cls.get_property_unit_info(property_unit).model_dump()
