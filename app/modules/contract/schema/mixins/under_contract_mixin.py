from uuid import UUID
from datetime import datetime
from typing import Optional


# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# schemas
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema


class UnderContractBase(BaseSchema):
    property_unit_assoc_id: Optional[UUID] = None
    contract_status: Optional[ContractStatusEnum]
    contract_number: Optional[str] = None
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    start_date: datetime
    end_date: datetime
    next_payment_due: datetime
    # properties: Optional[List[Union[Property, PropertyUnit]]] = Field(default_factory=list)
    # employee_representative: Optional[List[UserBase]] = Field(default_factory=list)
    # client_representative: Optional[List[UserBase]] = Field(default_factory=list)


class UnderContract(UnderContractBase):
    under_contract_id: Optional[UUID] = None


class UnderContractInfoMixin:
    # base attributes
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_number = f"CTR-{BaseFaker.bothify(text='#####')}"
    _start_date = BaseFaker.date_this_year()
    _end_date = BaseFaker.future_date()
    _next_payment_due = BaseFaker.future_datetime()

    _under_contract_create_json = {
        "property_unit_assoc_id": str(BaseFaker.uuid4()),
        "contract_status": _contract_status,
        "contract_number": _contract_number,
        "client_id": str(BaseFaker.uuid4()),
        "employee_id": str(BaseFaker.uuid4()),
        "start_date": _start_date.isoformat(),
        "end_date": _end_date.isoformat(),
        "next_payment_due": _next_payment_due.isoformat(),
    }

    _under_contract_update_json = {
        "property_unit_assoc_id": str(BaseFaker.uuid4()),
        "contract_status": _contract_status,
        "contract_number": _contract_number,
        "client_id": str(BaseFaker.uuid4()),
        "employee_id": str(BaseFaker.uuid4()),
        "start_date": _start_date.isoformat(),
        "end_date": _end_date.isoformat(),
        "next_payment_due": _next_payment_due.isoformat(),
    }
