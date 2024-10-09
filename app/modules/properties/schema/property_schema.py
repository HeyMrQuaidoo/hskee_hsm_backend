from pydantic import UUID4
from typing import List, Optional

# schema
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.address.schema.address_schema import AddressBase
from app.modules.address.schema.address_mixin import AddressMixin
from app.modules.properties.schema.mixins.property_mixin import PropertyInfoMixin

# models
from app.modules.properties.models.property import Property as PropertyModel


class PropertyUnitAssocBase(BaseSchema):
    property_unit_assoc_id: UUID4
    property_unit_type: str


class PropertyBase(BaseSchema):
    name: str
    address_id: Optional[UUID4] = None
    property_type: str
    amount: float
    security_deposit: float
    commission: float
    floor_space: float
    num_units: int
    num_bathrooms: int
    num_garages: int
    has_balconies: bool
    has_parking_space: bool
    pets_allowed: bool
    description: str
    property_status: str
    address: Optional[List[AddressBase]] = []


class Property(PropertyUnitAssocBase):
    property_unit_assoc_id: UUID4


class PropertyResponse(PropertyBase, PropertyInfoMixin):
    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property)


class PropertyCreateSchema(PropertyBase, PropertyInfoMixin, AddressMixin):
    address: Optional[List[AddressBase]]

    @classmethod
    def model_validate(cls, property: PropertyModel):
        return cls.get_property_info(property).model_dump()


class PropertyUpdateSchema(PropertyBase):
    address: Optional[List[AddressBase]]
