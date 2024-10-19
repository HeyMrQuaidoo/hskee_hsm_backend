from typing import Optional, List
from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict

# Enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# Base Faker
from app.modules.common.schema.base_schema import BaseFaker

# Schemas
from app.modules.contract.schema.mixins.under_contract_mixin import UnderContractBase
from app.modules.contract.schema.mixins.contract_mixin import ContractBase
from app.modules.properties.schema.property_schema import PropertyBase
from app.modules.auth.schema.user_schema import UserBase

# Models
from app.modules.contract.models.under_contract import UnderContract as UnderContractModel


class UnderContractCreateSchema(UnderContractBase):
    property_unit_assoc_id: UUID
    contract_status: ContractStatusEnum
    contract_number: str
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    start_date: datetime
    end_date: datetime
    next_payment_due: datetime

    # Faker attributes
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_number = f"CTR-{BaseFaker.bothify(text='#####')}"
    _start_date = BaseFaker.date_this_year()
    _end_date = BaseFaker.future_date()
    _next_payment_due = BaseFaker.future_datetime()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "property_unit_assoc_id": str(BaseFaker.uuid4()),
                "contract_status": _contract_status,
                "contract_number": _contract_number,
                "client_id": str(BaseFaker.uuid4()),
                "employee_id": str(BaseFaker.uuid4()),
                "start_date": _start_date.isoformat(),
                "end_date": _end_date.isoformat(),
                "next_payment_due": _next_payment_due.isoformat(),
            }
        }
    )


class UnderContractUpdateSchema(UnderContractBase):
    property_unit_assoc_id: Optional[UUID] = None
    contract_status: Optional[ContractStatusEnum] = None
    contract_number: Optional[str] = None
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    next_payment_due: Optional[datetime] = None

    # Faker attributes
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_number = f"CTR-{BaseFaker.bothify(text='#####')}"
    _start_date = BaseFaker.date_this_year()
    _end_date = BaseFaker.future_date()
    _next_payment_due = BaseFaker.future_datetime()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "property_unit_assoc_id": str(BaseFaker.uuid4()),
                "contract_status": _contract_status,
                "contract_number": _contract_number,
                "client_id": str(BaseFaker.uuid4()),
                "employee_id": str(BaseFaker.uuid4()),
                "start_date": _start_date.isoformat(),
                "end_date": _end_date.isoformat(),
                "next_payment_due": _next_payment_due.isoformat(),
            }
        }
    )


class UnderContractResponse(UnderContractBase):
    under_contract_id: UUID
    properties: Optional[PropertyBase] = None
    contract: Optional['Contract'] = None  # Use the appropriate Contract schema
    client_representative: Optional[UserBase] = None
    employee_representative: Optional[UserBase] = None

    @classmethod
    def model_validate(cls, under_contract: UnderContractModel):
        return cls(
            under_contract_id=under_contract.under_contract_id,
            property_unit_assoc_id=under_contract.property_unit_assoc_id,
            contract_status=under_contract.contract_status,
            contract_number=under_contract.contract_number,
            client_id=under_contract.client_id,
            employee_id=under_contract.employee_id,
            start_date=under_contract.start_date,
            end_date=under_contract.end_date,
            next_payment_due=under_contract.next_payment_due,
            properties=PropertyBase.model_validate(under_contract.properties) if under_contract.properties else None,
            contract=ContractBase.model_validate(under_contract.contract) if under_contract.contract else None,
            client_representative=UserBase.model_validate(under_contract.client_representative) if under_contract.client_representative else None,
            employee_representative=UserBase.model_validate(under_contract.employee_representative) if under_contract.employee_representative else None,
        ).model_dump()
