import uuid
from datetime import date
from pydantic import ConfigDict

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.address.schema.address_mixin import AddressMixin
from app.modules.properties.schema.mixins.property_mixin import (
    PropertyUnitBase,
    PropertyUnitInfoMixin,
)

# models
from app.modules.properties.models.unit import Units as UnitModel


class UnitResponse(PropertyUnitBase, PropertyUnitInfoMixin):
    @classmethod
    def model_validate(cls, property_unit: UnitModel):
        return cls.get_property_unit_info(property_unit)


class UnitCreateSchema(PropertyUnitBase, PropertyUnitInfoMixin, AddressMixin):
    # Faker attrributes
    _property_type = BaseFaker.random_choices(
        ["residential", "commercial", "industrial"], length=1
    )
    _property_status = BaseFaker.random_choices(
        ["sold", "rent", "lease", "bought", "available", "unavailable"], length=1
    )
    _property_unit_status = BaseFaker.random_choices(
        ["sold", "rent", "lease", "bought", "available", "unavailable"], length=1
    )
    _amount = round(BaseFaker.random_number(digits=5), 2)
    _security_deposit = round(BaseFaker.random_number(digits=4), 2)
    _commission = round(BaseFaker.random_number(digits=3), 2)
    _floor_space = BaseFaker.random_number(digits=3)
    _address_type = BaseFaker.random_choices(["billing", "mailing"], length=1)

    # Model configuration with Faker-generated example
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "property_id": str(uuid.uuid4()),
                "property_unit_code": f"Unit {BaseFaker.random_letter().upper()}{BaseFaker.random_digit()}",
                "property_unit_floor_space": BaseFaker.random_int(min=50, max=150),
                "property_unit_amount": BaseFaker.random_number(digits=4),
                "property_floor_id": BaseFaker.random_int(min=1, max=5),
                "property_status": _property_unit_status[0],
                "property_unit_notes": BaseFaker.sentence(),
                "property_unit_security_deposit": BaseFaker.random_number(digits=3),
                "property_unit_commission": BaseFaker.random_number(digits=2),
                "has_amenities": BaseFaker.boolean(),
            }
        },
    )

    @classmethod
    def model_validate(cls, property_unit: UnitModel):
        return cls.get_property_unit_info(property_unit).model_dump()


class UnitUpdateSchema(PropertyUnitBase):
    pass
