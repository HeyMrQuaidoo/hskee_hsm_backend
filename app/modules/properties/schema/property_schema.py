from typing import Optional
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
    _amount = round(BaseFaker.random_number(digits=5), 2)
    _security_deposit = round(BaseFaker.random_number(digits=4), 2)
    _commission = round(BaseFaker.random_number(digits=3), 2)
    _floor_space = BaseFaker.random_number(digits=3)
    _address_type = BaseFaker.random_choices(["billing", "mailing"], length=1)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "name": BaseFaker.company(),
                "property_type": _property_type[0],
                "amount": _amount,
                "security_deposit": _security_deposit,
                "commission": _commission,
                "floor_space": _floor_space,
                "num_units": BaseFaker.random_int(min=1, max=10),
                "num_bathrooms": BaseFaker.random_int(min=1, max=4),
                "num_garages": BaseFaker.random_int(min=0, max=2),
                "has_balconies": BaseFaker.boolean(),
                "has_parking_space": BaseFaker.boolean(),
                "pets_allowed": BaseFaker.boolean(),
                "description": BaseFaker.text(max_nb_chars=200),
                "property_status": _property_status[0],
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
                "amenities": [
                    {
                        "amenity_name": BaseFaker.word(),
                        "amenity_short_name": BaseFaker.word(),
                        "amenity_description": BaseFaker.sentence(),
                    },
                ]
            }
        },
    )

    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property).model_dump()


class PropertyUpdateSchema(PropertyBase, PropertyInfoMixin, AddressMixin):
    # Faker attributes
    _property_type: Optional[str] = BaseFaker.random_choices(
        ["residential", "commercial", "industrial"], length=1
    )[0]
    _property_status: Optional[str] = BaseFaker.random_choices(
        ["sold", "rent", "lease", "bought", "available", "unavailable"], length=1
    )[0]
    _property_unit_status: Optional[str] = BaseFaker.random_choices(
        ["sold", "rent", "lease", "bought", "available", "unavailable"], length=1
    )[0]
    _amount: Optional[float] = round(BaseFaker.random_number(digits=5), 2)
    _security_deposit: Optional[float] = round(BaseFaker.random_number(digits=4), 2)
    _commission: Optional[float] = round(BaseFaker.random_number(digits=3), 2)
    _floor_space: Optional[int] = BaseFaker.random_number(digits=3)
    _address_type: Optional[str] = BaseFaker.random_choices(["billing", "mailing"], length=1)[0]

    # Media faker attributes
    _media_name: Optional[str] = BaseFaker.word()
    _media_type: Optional[str] = BaseFaker.random_choices(
        ["image", "video", "audio", "document"], length=1
    )[0]
    _content_url: Optional[str] = BaseFaker.url()
    _is_thumbnail: Optional[bool] = BaseFaker.boolean()
    _caption: Optional[str] = BaseFaker.sentence()
    _description: Optional[str] = BaseFaker.text(max_nb_chars=200)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "name": Optional[str],
                "property_type": Optional[str],
                "amount": Optional[float],
                "security_deposit": Optional[float],
                "commission": Optional[float],
                "floor_space": Optional[int],
                "num_units": Optional[int],
                "num_bathrooms": Optional[int],
                "num_garages": Optional[int],
                "has_balconies": Optional[bool],
                "has_parking_space": Optional[bool],
                "pets_allowed": Optional[bool],
                "description": Optional[str],
                "property_status": Optional[str],
                "address": [
                    {
                        "address_1": Optional[str],
                        "address_2": Optional[str],
                        "address_postalcode": Optional[str],
                        "address_type": Optional[str],
                        "city": Optional[str],
                        "country": Optional[str],
                        "primary": Optional[bool],
                        "emergency_address": Optional[bool],
                        "region": Optional[str],
                    }
                ],
                "units": [
                    {
                        "property_unit_code": Optional[str],
                        "property_unit_floor_space": Optional[int],
                        "property_unit_amount": Optional[float],
                        "property_floor_id": Optional[int],
                        "property_status": Optional[str],
                        "property_unit_notes": Optional[str],
                        "property_unit_security_deposit": Optional[float],
                        "property_unit_commission": Optional[float],
                        "has_amenities": Optional[bool],
                        "property_unit_assoc_id": Optional[str],
                    },
                ],
                "media": [
                    {
                        "media_name": Optional[str],
                        "media_type": Optional[str],
                        "content_url": Optional[str],
                        "is_thumbnail": Optional[bool],
                        "caption": Optional[str],
                        "description": Optional[str],
                    }
                ],
                "amenities": [
                    {
                        "amenity_name": Optional[str],
                        "amenity_short_name": Optional[str],
                        "amenity_description": Optional[str],
                    },
                ]
            }
        },
    )

    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property)