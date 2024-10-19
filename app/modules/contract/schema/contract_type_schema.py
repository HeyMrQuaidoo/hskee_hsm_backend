from pydantic import BaseModel, ConfigDict
from typing import Optional
from decimal import Decimal
from app.modules.contract.models.contract_type import ContractType as ContractTypeModel
from app.modules.common.schema.base_schema import BaseFaker  # Importing BaseFaker

class ContractTypeBase(BaseModel):
    contract_type_name: str
    fee_percentage: Decimal


class ContractTypeCreateSchema(ContractTypeBase):
    # Adding BaseFaker to auto-generate example values
    _contract_type_name = BaseFaker.random_element(["Annual", "Monthly", "Weekly"])
    _fee_percentage = round(BaseFaker.random_number(digits=3), 2)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "contract_type_name": _contract_type_name,
                "fee_percentage": _fee_percentage,
            }
        }
    )
    @classmethod
    def model_validate(cls, contract_type: ContractTypeModel):
        return cls(
            contract_type_id=contract_type.contract_type_id,
            contract_type_name=contract_type.contract_type_name,
            fee_percentage=contract_type.fee_percentage,
        ).model_dump()


class ContractTypeUpdateSchema(ContractTypeBase):
    contract_type_name: Optional[str] = None
    fee_percentage: Optional[Decimal] = None

    # Adding BaseFaker to auto-generate example values
    _contract_type_name = BaseFaker.random_element(["Monthly", "Weekly", "One-time"])
    _fee_percentage = round(BaseFaker.random_number(digits=3), 2)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "contract_type_name": _contract_type_name,
                "fee_percentage": _fee_percentage,
            }
        }
    )
    @classmethod
    def model_validate(cls, contract_type: ContractTypeModel):
        return cls(
            contract_type_id=contract_type.contract_type_id,
            contract_type_name=contract_type.contract_type_name,
            fee_percentage=contract_type.fee_percentage,
        ).model_dump()


class ContractTypeResponse(ContractTypeBase):
    contract_type_id: int

    # Adding BaseFaker to auto-generate example values
    _contract_type_id = BaseFaker.random_int(min=1, max=100)
    _contract_type_name = BaseFaker.random_element(["Monthly", "Weekly", "One-time"])
    _fee_percentage = round(BaseFaker.random_number(digits=3), 2)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "contract_type_id": _contract_type_id,
                "contract_type_name": _contract_type_name,
                "fee_percentage": _fee_percentage,
            }
        },
        from_attributes=True
    )

    @classmethod
    def model_validate(cls, contract_type: ContractTypeModel):
        return cls(
            contract_type_id=contract_type.contract_type_id,
            contract_type_name=contract_type.contract_type_name,
            fee_percentage=contract_type.fee_percentage,
        ).model_dump()