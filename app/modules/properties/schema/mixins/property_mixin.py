from uuid import UUID
from pydantic import UUID4
from typing import List, Optional, Union

# enums
from app.modules.properties.enums.property_enums import PropertyStatus, PropertyType

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.address.schema.address_schema import AddressBase
from app.modules.address.schema.address_mixin import AddressMixin
from app.modules.resources.schema.mixins.amenities_mixin import AmenityBase

# models
from app.modules.properties.models.property_unit_association import (
    PropertyUnitAssoc as PropertyUnitAssocModel,
)


class PropertyUnitBase(BaseSchema):
    property_id: Optional[UUID] = None
    property_unit_code: Optional[str] = None
    property_unit_floor_space: Optional[int] = None
    property_unit_amount: Optional[float] = None
    property_floor_id: Optional[int] = None
    property_status: PropertyStatus
    property_unit_notes: Optional[str] = None
    property_unit_security_deposit: Optional[float] = None
    property_unit_commission: Optional[float] = None
    has_amenities: Optional[bool] = False


class PropertyUnit(PropertyUnitBase):
    property_unit_assoc_id: Optional[UUID]


class PropertyUnitInfoMixin:
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

    _unit_create_json = {
        "property_id": str(BaseFaker.uuid4()),
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

    _unit_update_json = {
        "property_id": str(BaseFaker.uuid4()),
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

    @classmethod
    def get_property_unit_info(
        cls, property_unit: Union[PropertyUnit | List[PropertyUnit]]
    ) -> PropertyUnit:
        result = []

        if not isinstance(property_unit, list):
            return PropertyUnit(
                property_unit_assoc_id=property_unit.property_unit_assoc_id,
                property_unit_code=property_unit.property_unit_code,
                property_unit_floor_space=property_unit.property_unit_floor_space,
                property_unit_amount=property_unit.property_unit_amount,
                property_floor_id=property_unit.property_floor_id,
                property_unit_notes=property_unit.property_unit_notes,
                has_amenities=property_unit.has_amenities,
                property_id=property_unit.property_id,
                property_unit_security_deposit=property_unit.property_unit_security_deposit,
                property_unit_commission=property_unit.property_unit_commission,
                property_status=property_unit.property_status,
            )
        else:
            for property_unit_item in property_unit:
                result.append(
                    PropertyUnit(
                        property_unit_assoc_id=property_unit_item.property_unit_assoc_id,
                        property_unit_code=property_unit_item.property_unit_code,
                        property_unit_floor_space=property_unit_item.property_unit_floor_space,
                        property_unit_amount=property_unit_item.property_unit_amount,
                        property_floor_id=property_unit_item.property_floor_id,
                        property_unit_notes=property_unit_item.property_unit_notes,
                        has_amenities=property_unit_item.has_amenities,
                        property_id=property_unit_item.property_id,
                        property_unit_security_deposit=property_unit_item.property_unit_security_deposit,
                        property_unit_commission=property_unit_item.property_unit_commission,
                        property_status=property_unit_item.property_status,
                    )
                )
        return result


class PropertyBase(BaseSchema):
    name: str
    property_type: PropertyType
    amount: float
    security_deposit: Optional[float]
    commission: Optional[float]
    floor_space: Optional[float]
    num_units: Optional[int]
    num_bathrooms: Optional[int]
    num_garages: Optional[int]
    has_balconies: Optional[bool] = False
    has_parking_space: Optional[bool] = False
    pets_allowed: bool = False
    description: Optional[str] = None
    property_status: PropertyStatus
    address: Optional[List[AddressBase]] = []
    units: Optional[List[PropertyUnit] | List[PropertyUnitBase]] = []
    amenities: Optional[List[AmenityBase] | List[AmenityBase]] = []


class Property(PropertyBase):
    property_unit_assoc_id: Optional[UUID]


class PropertyUnitAssocBase(BaseSchema):
    property_unit_assoc_id: UUID4
    property_unit_type: str


class PropertyInfoMixin(AddressMixin, PropertyUnitInfoMixin):
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

    # media faker attributes
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_choices(
        ["image", "video", "audio", "document"], length=1
    )
    _content_url = BaseFaker.url()
    _is_thumbnail = BaseFaker.boolean()
    _caption = BaseFaker.sentence()
    _description = BaseFaker.text(max_nb_chars=200)

    # amenitites faker attributes
    _amenity_name = BaseFaker.word()
    _amenity_short_name = BaseFaker.word()
    _description = BaseFaker.sentence()

    _property_create_json = {
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
                "property_unit_floor_space": BaseFaker.random_int(min=50, max=150),
                "property_unit_amount": BaseFaker.random_number(digits=4),
                "property_floor_id": BaseFaker.random_int(min=1, max=5),
                "property_status": _property_unit_status[0],
                "property_unit_notes": BaseFaker.sentence(),
                "property_unit_security_deposit": BaseFaker.random_number(digits=3),
                "property_unit_commission": BaseFaker.random_number(digits=2),
                "has_amenities": BaseFaker.boolean(),
            },
        ],
        "media": [
            {
                "media_name": BaseFaker.word(),
                "media_type": BaseFaker.random_choices(
                    ["image", "video", "audio", "document"]
                )[0],
                "content_url": BaseFaker.url(),
                "is_thumbnail": BaseFaker.boolean(),
                "caption": BaseFaker.sentence(),
                "description": BaseFaker.text(max_nb_chars=200),
            }
        ],
        "amenities": [
            {
                "amenity_name": BaseFaker.word(),
                "amenity_short_name": BaseFaker.word(),
                "amenity_description": BaseFaker.sentence(),
            },
        ],
    }

    _property_update_json = {
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
                "property_unit_floor_space": BaseFaker.random_int(min=50, max=150),
                "property_unit_amount": BaseFaker.random_number(digits=4),
                "property_floor_id": BaseFaker.random_int(min=1, max=5),
                "property_status": _property_unit_status[0],
                "property_unit_notes": BaseFaker.sentence(),
                "property_unit_security_deposit": BaseFaker.random_number(digits=3),
                "property_unit_commission": BaseFaker.random_number(digits=2),
                "has_amenities": BaseFaker.boolean(),
                "property_unit_assoc_id": "06ff99dd-d3a7-454d-98ff-39dd8894f92f",
            },
        ],
        "media": [
            {
                "media_name": _media_name,
                "media_type": _media_type[0],
                "content_url": _content_url,
                "is_thumbnail": _is_thumbnail,
                "caption": _caption,
                "description": _description,
            }
        ],
        "amenities": [
            {
                "amenity_name": _amenity_name,
                "amenity_short_name": _amenity_short_name,
                "description": _description,
            }
        ],
    }

    @classmethod
    def get_property_info(cls, property: Property) -> Property:
        return Property(
            property_unit_assoc_id=property.property_unit_assoc_id,
            name=property.name,
            property_type=property.property_type,
            amount=property.amount,
            security_deposit=property.security_deposit,
            commission=property.commission,
            floor_space=property.floor_space,
            num_units=property.num_units,
            num_bathrooms=property.num_bathrooms,
            num_garages=property.num_garages,
            has_balconies=property.has_balconies,
            has_parking_space=property.has_parking_space,
            pets_allowed=property.pets_allowed,
            description=property.description,
            property_status=property.property_status,
            address=cls.get_address_base(property.address),
            units=cls.get_property_unit_info(property.units),
            amenities=property.amenities,
        ).model_dump()


class PropertyDetailsMixin(PropertyInfoMixin, PropertyUnitInfoMixin):
    _PROPERTY_TYPE_DEFAULT: str = "Units"

    # @classmethod
    # def get_property_details_from_contract(cls, contract_details: List[ContractModel]):
    #     """
    #     Extract and format property details from a list of contract models.

    #     This method iterates over the provided contract models, extracting and converting
    #     property unit associations to their corresponding details based on their type (either
    #     'Units' or other types).

    #     Args:
    #         contract_details (List[ContractModel]): A list of contract models from which property
    #         details are extracted.
    #     """
    #     result = []

    #     for contract in contract_details:
    #         result.append(cls.get_property_details(contract.properties))

    #     return result

    @classmethod
    def get_property_details(
        cls,
        property_unit_assoc_details: Union[
            PropertyUnitAssocModel | List[PropertyUnitAssocModel]
        ],
    ) -> List[Union[Property, PropertyUnit]]:
        result = []

        property_unit_assoc_details = (
            [property_unit_assoc_details]
            if not isinstance(property_unit_assoc_details, list)
            else property_unit_assoc_details
        )

        for property_unit_assoc in property_unit_assoc_details:
            if not property_unit_assoc:
                continue
            if (
                property_unit_assoc.property_unit_type
                == PropertyDetailsMixin._PROPERTY_TYPE_DEFAULT
            ):
                result.append(cls.get_property_unit_info(property_unit_assoc))
            else:
                result.append(cls.get_property_info(property_unit_assoc))
        return result
