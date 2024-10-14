from uuid import UUID
from pydantic import UUID4
from typing import List, Optional, Union

# enums
from app.modules.properties.enums.property_enums import PropertyStatus, PropertyType

# schema
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
