from uuid import UUID
from typing import List, Optional, Union

# Enums
from app.modules.properties.enums.property_enums import PropertyStatus, PropertyType
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.address.enums.address_enums import AddressTypeEnum as AddressType

# Base schema
from app.modules.common.schema.base_schema import BaseSchema

# Models (Assuming these models are imported correctly)
from app.modules.properties.models.property_unit_association import (
    PropertyUnitAssoc as PropertyUnitAssocModel,
)
from app.modules.properties.models.property import Property as PropertyModel
from app.modules.properties.models.unit import Units as UnitsModel
from app.modules.resources.models.media import Media as MediaModel
from app.modules.address.models.address import Addresses as AddressModel
from app.modules.resources.models.amenity import Amenities as AmenityModel
from app.modules.billing.models.utility import Utilities as UtilitiesModel
from app.modules.associations.models.entity_billable import EntityBillable as EntityBillableModel
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel


# from uuid import UUID
from pydantic import UUID4
# from typing import List, Optional, Union

# # enums
# from app.modules.properties.enums.property_enums import PropertyStatus, PropertyType

# # schema
# from app.modules.common.schema.base_schema import BaseSchema
# from app.modules.address.schema.address_schema import AddressBase
# from app.modules.address.schema.address_mixin import AddressMixin
# from app.modules.resources.schema.amenities_schema import AmenityBase

# # models
# from app.modules.properties.models.property_unit_association import (
#     PropertyUnitAssoc as PropertyUnitAssocModel,
# )

# Media Mixins and Classes
class MediaBase(BaseSchema):
    media_name: Optional[str] = None
    media_type: Optional[MediaType] = None
    content_url: Optional[str] = None
    is_thumbnail: Optional[bool] = False
    caption: Optional[str] = None
    description: Optional[str] = None

class Media(MediaBase):
    media_id: UUID

class MediaMixin:
    @classmethod
    def get_media_info(cls, media_list: List[MediaModel]) -> List[Media]:
        result = []
        for media in media_list:
            result.append(
                Media(
                    media_id=media.media_id,
                    media_name=media.media_name,
                    media_type=media.media_type,
                    content_url=media.content_url,
                    is_thumbnail=media.is_thumbnail,
                    caption=media.caption,
                    description=media.description,
                )
            )
        return result

# Address Mixins and Classes
class AddressBase(BaseSchema):
    address_1: str
    address_2: Optional[str] = None
    address_postalcode: Optional[str] = None
    address_type: AddressType
    city: str
    country: str
    primary: bool
    emergency_address: bool
    region: str

class AddressMixin:
    @classmethod
    def get_address_info(cls, address_list: List[AddressModel]) -> List[AddressBase]:
        result = []
        for address in address_list:
            result.append(
                AddressBase(
                    address_1=address.address_1,
                    address_2=address.address_2,
                    address_postalcode=address.address_postalcode,
                    address_type=address.address_type,
                    city=address.city,
                    country=address.country,
                    primary=address.primary,
                    emergency_address=address.emergency_address,
                    region=address.region,
                )
            )
        return result

# Utility Mixins and Classes
class UtilityInfo(BaseSchema):
    utility: str
    frequency: str
    billable_amount: float
    apply_to_units: bool
    entity_billable_id: UUID

class UtilitiesMixin:
    @classmethod
    def get_utilities_info(cls, utilities: List[EntityBillableModel]) -> List[UtilityInfo]:
        result = []
        for entity_utility in utilities:
            utility: UtilitiesModel = entity_utility.utility
            payment_type: PaymentTypeModel = entity_utility.payment_type
            result.append(
                UtilityInfo(
                    utility=utility.name,
                    frequency=payment_type.payment_type_name,
                    billable_amount=entity_utility.billable_amount,
                    apply_to_units=entity_utility.apply_to_units,
                    entity_billable_id=entity_utility.entity_billable_id,
                )
            )
        return result

# Amenity Mixins and Classes
class AmenityInfo(BaseSchema):
    amenity_name: str
    amenity_short_name: str
    description: Optional[str] = None

class AmenitiesMixin:
    @classmethod
    def get_amenities_info(cls, amenities: List[AmenityModel]) -> List[AmenityInfo]:
        result = []
        for amenity in amenities:
            result.append(
                AmenityInfo(
                    amenity_name=amenity.amenity_name,
                    amenity_short_name=amenity.amenity_short_name,
                    description=amenity.description,
                )
            )
        return result

# Property Unit Mixins and Classes
class PropertyUnitBase(BaseSchema):
    property_id: Optional[UUID] = None
    property_unit_code: Optional[str] = None
    property_unit_floor_space: Optional[float] = None
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
        cls, property_units: Union[UnitsModel, List[UnitsModel]]
    ) -> Union[PropertyUnit, List[PropertyUnit]]:
        result = []
        if not isinstance(property_units, list):
            property_units = [property_units]

        for unit in property_units:
            result.append(
                PropertyUnit(
                    property_unit_assoc_id=unit.property_unit_assoc_id,
                    property_unit_code=unit.property_unit_code,
                    property_unit_floor_space=unit.property_unit_floor_space,
                    property_unit_amount=unit.property_unit_amount,
                    property_floor_id=unit.property_floor_id,
                    property_status=unit.property_status,
                    property_unit_notes=unit.property_unit_notes,
                    property_unit_security_deposit=unit.property_unit_security_deposit,
                    property_unit_commission=unit.property_unit_commission,
                    has_amenities=unit.has_amenities,
                    property_id=unit.property_id,
                )
            )
        return result if len(result) > 1 else result[0]

# Property Mixins and Classes
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

class Property(PropertyBase):
    property_unit_assoc_id: Optional[UUID]
    address: Optional[List[AddressBase]] = []
    units: Optional[List[PropertyUnit]] = []
    amenities: Optional[List[AmenityInfo]] = []
    media: Optional[List[Media]] = []
    utilities: Optional[List[UtilityInfo]] = []
    is_contract_active: Optional[bool] = False

class PropertyInfoMixin(
    MediaMixin, AddressMixin, UtilitiesMixin, AmenitiesMixin, PropertyUnitInfoMixin
):
    @classmethod
    def get_property_info(cls, property: PropertyModel) -> Property:
        # Extract media information
        media_info = cls.get_media_info(property.media) if property.media else []

        # Extract units information
        units_info = cls.get_property_unit_info(property.units) if property.units else []

        # Extract amenities information
        amenities_info = (
            cls.get_amenities_info(property.amenities) if property.amenities else []
        )

        # Extract address information
        address_info = cls.get_address_info(property.address) if property.address else []

        # Extract utilities information
        utilities_info = (
            cls.get_utilities_info(property.utilities) if property.utilities else []
        )

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
            address=address_info,
            units=units_info,
            amenities=amenities_info,
            media=media_info,
            utilities=utilities_info,
            is_contract_active=property.is_contract_active,
        )


class Property(PropertyBase):
    property_unit_assoc_id: Optional[UUID]


class PropertyUnitAssocBase(BaseSchema):
    property_unit_assoc_id: UUID4
    property_unit_type: str

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