from uuid import UUID
from datetime import datetime
from typing import Any, List, Optional, Union


from app.modules.common.schema.base_schema import BaseSchema
from app.modules.address.schema.address_schema import AddressBase
from app.modules.address.schema.address_mixin import AddressMixin

from app.modules.properties.models.rental_history import (
    PastRentalHistory as PastRentalHistoryModel,
)


class PastRentalHistoryBase(BaseSchema):
    property_owner_name: str
    property_owner_email: str
    property_owner_mobile: str
    start_date: datetime
    end_date: datetime
    user_id: Optional[UUID] = None
    address: Optional[List[AddressBase]] = []


class PastRentalHistory(PastRentalHistoryBase, AddressMixin):
    rental_history_id: UUID

    @classmethod
    def model_validate(cls, rental_history: PastRentalHistoryModel):
        return cls(
            rental_history_id=rental_history.rental_history_id,
            property_owner_name=rental_history.property_owner_name,
            property_owner_email=rental_history.property_owner_email,
            property_owner_mobile=rental_history.property_owner_mobile,
            start_date=rental_history.start_date,
            end_date=rental_history.end_date,
            user_id=rental_history.user_id,
            address=cls.get_address_base(rental_history.address),
        ).model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude_defaults=True,
            exclude=["user_id"],
        )


class PastRentalHistoryResponse(BaseSchema, AddressMixin):
    rental_history_id: Optional[UUID | Any] = None
    property_owner_name: str = None
    property_owner_email: str = None
    property_owner_mobile: Union[str | int] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    user_id: Optional[UUID] = None
    address: Optional[List[AddressBase]] = []

    @classmethod
    def model_validate(cls, rental_history: PastRentalHistoryModel):
        return cls(
            rental_history_id=rental_history.rental_history_id,
            property_owner_name=rental_history.property_owner_name,
            property_owner_email=rental_history.property_owner_email,
            property_owner_mobile=rental_history.property_owner_mobile,
            start_date=rental_history.start_date,
            end_date=rental_history.end_date,
            user_id=rental_history.user_id,
            address=cls.get_address_base(rental_history.address),
        ).model_dump()  # exclude_none=True, exclude_unset=True, exclude_defaults=True
