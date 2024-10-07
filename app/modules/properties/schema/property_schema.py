from datetime import date
from pydantic import ConfigDict

# schema
from app.modules.common.schema.base_schema import BaseFaker
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
    _amount = round(
        BaseFaker.random_number(digits=5), 2
    )  # Random property price or rent
    _security_deposit = round(
        BaseFaker.random_number(digits=4), 2
    )  # Random security deposit
    _commission = round(
        BaseFaker.random_number(digits=3), 2
    )  # Random commission amount
    _floor_space = BaseFaker.random_number(
        digits=3
    )  # Random floor space in square feet/meters
    _address_type = BaseFaker.random_choices(["billing", "mailing"], length=1)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "name": BaseFaker.company(),  # Random company name or property name
                "property_type": _property_type[
                    0
                ],  # Random property type from the list
                "amount": _amount,  # Random price or rent
                "security_deposit": _security_deposit,  # Random security deposit
                "commission": _commission,  # Random commission
                "floor_space": _floor_space,  # Random floor space
                "num_units": BaseFaker.random_int(
                    min=1, max=10
                ),  # Random number of units
                "num_bathrooms": BaseFaker.random_int(
                    min=1, max=4
                ),  # Random number of bathrooms
                "num_garages": BaseFaker.random_int(
                    min=0, max=2
                ),  # Random number of garages
                "has_balconies": BaseFaker.boolean(),  # Random boolean for balconies
                "has_parking_space": BaseFaker.boolean(),  # Random boolean for parking space
                "pets_allowed": BaseFaker.boolean(),  # Random boolean for pets allowed
                "description": BaseFaker.text(max_nb_chars=200),  # Random description
                "property_status": _property_status[0],  # Random property status
                "address": [
                    {
                        "address_1": BaseFaker.address(),
                        "address_2": BaseFaker.street_address(),
                        "address_postalcode": "",
                        "address_type": _address_type[0],
                        "city": BaseFaker.city(),
                        "country": BaseFaker.country(),
                        "primary": True,
                        "emergency_address": False,
                        "region": BaseFaker.state(),
                    }
                ],
                "units": [
                    {
                        "property_unit_code": f"Unit {BaseFaker.random_letter().upper()}{BaseFaker.random_digit()}",
                        "property_unit_floor_space": BaseFaker.random_int(
                            min=50, max=150
                        ),
                        "property_unit_amount": BaseFaker.random_number(digits=4),
                        "property_floor_id": BaseFaker.random_int(min=1, max=5),
                        "property_status": _property_unit_status[0],
                        "property_unit_notes": BaseFaker.sentence(),
                        "property_unit_security_deposit": BaseFaker.random_number(
                            digits=3
                        ),
                        "property_unit_commission": BaseFaker.random_number(digits=2),
                        "has_amenities": BaseFaker.boolean(),
                    },
                ],
            }
        },
    )

    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property).model_dump()


class PropertyUpdateSchema(PropertyBase, PropertyInfoMixin, AddressMixin):
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
    _amount = round(
        BaseFaker.random_number(digits=5), 2
    )  # Random property price or rent
    _security_deposit = round(
        BaseFaker.random_number(digits=4), 2
    )  # Random security deposit
    _commission = round(
        BaseFaker.random_number(digits=3), 2
    )  # Random commission amount
    _floor_space = BaseFaker.random_number(
        digits=3
    )  # Random floor space in square feet/meters
    _address_type = BaseFaker.random_choices(["billing", "mailing"], length=1)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "name": BaseFaker.company(),  # Random company name or property name
                "property_type": _property_type[
                    0
                ],  # Random property type from the list
                "amount": _amount,  # Random price or rent
                "security_deposit": _security_deposit,  # Random security deposit
                "commission": _commission,  # Random commission
                "floor_space": _floor_space,  # Random floor space
                "num_units": BaseFaker.random_int(
                    min=1, max=10
                ),  # Random number of units
                "num_bathrooms": BaseFaker.random_int(
                    min=1, max=4
                ),  # Random number of bathrooms
                "num_garages": BaseFaker.random_int(
                    min=0, max=2
                ),  # Random number of garages
                "has_balconies": BaseFaker.boolean(),  # Random boolean for balconies
                "has_parking_space": BaseFaker.boolean(),  # Random boolean for parking space
                "pets_allowed": BaseFaker.boolean(),  # Random boolean for pets allowed
                "description": BaseFaker.text(max_nb_chars=200),  # Random description
                "property_status": _property_status[0],  # Random property status
                "address": [
                    {
                        "address_1": BaseFaker.address(),
                        "address_2": BaseFaker.street_address(),
                        "address_postalcode": "",
                        "address_type": _address_type[0],
                        "city": BaseFaker.city(),
                        "country": BaseFaker.country(),
                        "primary": True,
                        "emergency_address": False,
                        "region": BaseFaker.state(),
                    }
                ],
                "units": [
                    {
                        "property_unit_code": f"Unit {BaseFaker.random_letter().upper()}{BaseFaker.random_digit()}",
                        "property_unit_floor_space": BaseFaker.random_int(
                            min=50, max=150
                        ),
                        "property_unit_amount": BaseFaker.random_number(digits=4),
                        "property_floor_id": BaseFaker.random_int(min=1, max=5),
                        "property_status": _property_unit_status[0],
                        "property_unit_notes": BaseFaker.sentence(),
                        "property_unit_security_deposit": BaseFaker.random_number(
                            digits=3
                        ),
                        "property_unit_commission": BaseFaker.random_number(digits=2),
                        "has_amenities": BaseFaker.boolean(),
                        "property_unit_assoc_id": "06ff99dd-d3a7-454d-98ff-39dd8894f92f",
                    },
                ],
            }
        },
    )

    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property)
