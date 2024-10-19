# app/modules/properties/schema/property_schema.py

from datetime import date
from typing import Optional, List
from uuid import UUID
from pydantic import ConfigDict

# Enums
from app.modules.properties.enums.property_enums import PropertyType, PropertyStatus
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.address.enums.address_enums import AddressTypeEnum as AddressType

# Base Faker and Base Schema
from app.modules.common.schema.base_schema import BaseFaker

# Mixins and Base Classes
from app.modules.properties.schema.mixins.property_mixin import (
    PropertyBase,
    PropertyInfoMixin,
    PropertyUnitBase,
    PropertyUnit,
    MediaBase,
    AddressBase,
    AmenityInfo,
    UtilityInfo,
)

# Models
from app.modules.properties.models.property import Property as PropertyModel

class PropertyResponse(PropertyBase):
    property_id: UUID
    media: Optional[List[MediaBase]] = None
    units: Optional[List[PropertyUnit]] = None
    amenities: Optional[List[AmenityInfo]] = None
    address: Optional[List[AddressBase]] = None
    utilities: Optional[List[UtilityInfo]] = None
    is_contract_active: bool

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
    )

    @classmethod
    def model_validate(cls, property: PropertyModel):
        property_info = PropertyInfoMixin.get_property_info(property)
        return cls(**property_info.__dict__)

class PropertyCreateSchema(PropertyBase):
    media: Optional[List[MediaBase]] = None
    units: Optional[List[PropertyUnitBase]] = None
    amenities: Optional[List[AmenityInfo]] = None
    utilities: Optional[List[UtilityInfo]] = None
    address: Optional[List[AddressBase]] = None

    # Faker attributes
    _property_type = BaseFaker.random_choices(
        [e.value for e in PropertyType], length=1
    )
    _property_status = BaseFaker.random_choices(
        [e.value for e in PropertyStatus], length=1
    )
    _property_unit_status = BaseFaker.random_choices(
        [e.value for e in PropertyStatus], length=1
    )
    _amount = round(BaseFaker.random_number(digits=5), 2)
    _security_deposit = round(BaseFaker.random_number(digits=4), 2)
    _commission = round(BaseFaker.random_number(digits=3), 2)
    _floor_space = BaseFaker.random_number(digits=3)
    _address_type = BaseFaker.random_choices([e.value for e in AddressType], length=1)

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
                        "description": BaseFaker.sentence(),
                    },
                ],
                "media": [
                    {
                        "media_name": BaseFaker.word(),
                        "media_type": BaseFaker.random_element(
                            [e.value for e in MediaType]
                        ),
                        "content_url": BaseFaker.url(),
                        "is_thumbnail": BaseFaker.boolean(),
                        "caption": BaseFaker.sentence(),
                        "description": BaseFaker.text(max_nb_chars=200),
                    }
                ],
            }
        },
    )

class PropertyUpdateSchema(PropertyBase):
    name: Optional[str] = None
    property_type: Optional[PropertyType] = None
    amount: Optional[float] = None
    property_status: Optional[PropertyStatus] = None
    media: Optional[List[MediaBase]] = None
    units: Optional[List[PropertyUnitBase]] = None
    amenities: Optional[List[AmenityInfo]] = None
    utilities: Optional[List[UtilityInfo]] = None
    address: Optional[List[AddressBase]] = None

    # Faker attributes
    _property_type = BaseFaker.random_choices(
        [e.value for e in PropertyType], length=1
    )
    _property_status = BaseFaker.random_choices(
        [e.value for e in PropertyStatus], length=1
    )
    _property_unit_status = BaseFaker.random_choices(
        [e.value for e in PropertyStatus], length=1
    )
    _amount = round(BaseFaker.random_number(digits=5), 2)
    _security_deposit = round(BaseFaker.random_number(digits=4), 2)
    _commission = round(BaseFaker.random_number(digits=3), 2)
    _floor_space = BaseFaker.random_number(digits=3)
    _address_type = BaseFaker.random_choices([e.value for e in AddressType], length=1)

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
                        "property_unit_assoc_id": "06ff99dd-d3a7-454d-98ff-39dd8894f92f",
                    },
                ],
                "amenities": [
                    {
                        "amenity_name": BaseFaker.word(),
                        "amenity_short_name": BaseFaker.word(),
                        "description": BaseFaker.sentence(),
                    },
                ],
                "media": [
                    {
                        "media_name": BaseFaker.word(),
                        "media_type": BaseFaker.random_element(
                            [e.value for e in MediaType]
                        ),
                        "content_url": BaseFaker.url(),
                        "is_thumbnail": BaseFaker.boolean(),
                        "caption": BaseFaker.sentence(),
                        "description": BaseFaker.text(max_nb_chars=200),
                    }
                ],
            }
        },
    )

