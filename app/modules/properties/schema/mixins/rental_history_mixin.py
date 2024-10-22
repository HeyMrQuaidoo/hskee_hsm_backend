from uuid import UUID
from datetime import datetime
from typing import Optional, List, Union

# schema
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.address.schema.address_schema import AddressBase
from app.modules.address.schema.address_mixin import AddressMixin

# models
from app.modules.properties.models.rental_history import (
    PastRentalHistory as PastRentalHistoryModel,
)


class PastRentalHistoryBase(BaseSchema):
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    property_owner_name: str
    property_owner_email: str
    property_owner_mobile: str
    address: Optional[List[AddressBase]] = []


class PastRentalHistory(PastRentalHistoryBase, AddressMixin):
    rental_history_id: Optional[UUID]


class PastRentalHistoryMixin(PastRentalHistoryBase, AddressMixin):
    @classmethod
    def get_rental_history_info(
        cls,
        rental_histories: Union[PastRentalHistoryModel, List[PastRentalHistoryModel]],
    ) -> List[PastRentalHistoryModel]:
        result = []
        for history in rental_histories:
            history_obj = cls(
                rental_history_id=history.rental_history_id,
                start_date=history.start_date,
                end_date=history.end_date,
                user_id=history.user_id,
                property_owner_name=history.property_owner_name,
                property_owner_email=history.property_owner_email,
                property_owner_mobile=history.property_owner_mobile,
                address=cls.get_address_base(history.address),
            ).model_dump()

            result.append(history_obj)
        return result

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
