from pydantic import ConfigDict

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.contract.schema.mixins.contract_mixin import (
    ContractBase,
    ContractInfoMixin,
)
from app.modules.billing.schema.mixins.utility_mixin import UtilitiesMixin

# models
from app.modules.contract.models.contract import Contract as ContractModel


class ContractCreateSchema(ContractBase, ContractInfoMixin, UtilitiesMixin):
    # Faker attributes
    _contract_type_id = BaseFaker.random_int(min=1, max=5)
    _payment_type_id = BaseFaker.random_int(min=1, max=5)
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_details = BaseFaker.text(max_nb_chars=200)
    _num_invoices = BaseFaker.random_int(min=1, max=10)
    _payment_amount = round(BaseFaker.random_number(digits=5), 2)
    _fee_percentage = round(BaseFaker.random_number(digits=2), 2)
    _fee_amount = round(BaseFaker.random_number(digits=4), 2)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "contract_type_id": _contract_type_id,
                "payment_type_id": _payment_type_id,
                "contract_status": _contract_status,
                "contract_details": _contract_details,
                "num_invoices": _num_invoices,
                "payment_amount": _payment_amount,
                "fee_percentage": _fee_percentage,
                "fee_amount": _fee_amount,
                "date_signed": BaseFaker.date_this_year(),
                "start_date": BaseFaker.date_this_year(),
                "end_date": BaseFaker.future_date(),
            }
        },
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type=contract.contract_type_value,
            payment_type=contract.payment_type_value,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            contract_info=cls.get_contract_details(contract.under_contract),
            utilities=cls.get_utilities_info(contract.utilities),
        ).model_dump()


class ContractUpdateSchema(ContractBase, ContractInfoMixin, UtilitiesMixin):
    # Faker attributes for example
    _contract_type_id = BaseFaker.random_int(min=1, max=5)
    _payment_type_id = BaseFaker.random_int(min=1, max=5)
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_details = BaseFaker.text(max_nb_chars=200)
    _num_invoices = BaseFaker.random_int(min=1, max=10)
    _payment_amount = round(BaseFaker.random_number(digits=5), 2)
    _fee_percentage = round(BaseFaker.random_number(digits=2), 2)
    _fee_amount = round(BaseFaker.random_number(digits=4), 2)

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "contract_type_id": _contract_type_id,
                "payment_type_id": _payment_type_id,
                "contract_status": _contract_status,
                "contract_details": _contract_details,
                "num_invoices": _num_invoices,
                "payment_amount": _payment_amount,
                "fee_percentage": _fee_percentage,
                "fee_amount": _fee_amount,
                "date_signed": BaseFaker.date_this_year(),
                "start_date": BaseFaker.date_this_year(),
                "end_date": BaseFaker.future_date(),
            }
        },
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type=contract.contract_type_value,
            payment_type=contract.payment_type_value,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            contract_info=cls.get_contract_details(contract.under_contract),
            utilities=cls.get_utilities_info(contract.utilities),
        ).model_dump()


class ContractResponse(ContractBase, ContractInfoMixin, UtilitiesMixin):
    # Faker attributes for example
    _contract_number = BaseFaker.random_element(["C-12345", "C-67890"])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "contract_number": _contract_number,
                "contract_id": str(BaseFaker.uuid4()),
                "contract_type_id": BaseFaker.random_int(min=1, max=5),
                "payment_type_id": BaseFaker.random_int(min=1, max=5),
                "contract_status": BaseFaker.random_element(
                    [e.value for e in ContractStatusEnum]
                ),
                "contract_details": BaseFaker.text(max_nb_chars=200),
                "num_invoices": BaseFaker.random_int(min=1, max=10),
                "payment_amount": round(BaseFaker.random_number(digits=5), 2),
                "fee_percentage": round(BaseFaker.random_number(digits=2), 2),
                "fee_amount": round(BaseFaker.random_number(digits=4), 2),
                "date_signed": BaseFaker.date_this_year(),
                "start_date": BaseFaker.date_this_year(),
                "end_date": BaseFaker.future_date(),
            }
        },
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type=contract.contract_type_value,
            payment_type=contract.payment_type_value,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            contract_info=cls.get_contract_details(contract.under_contract),
            utilities=cls.get_utilities_info(contract.utilities),
        ).model_dump()
