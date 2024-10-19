from uuid import UUID
from decimal import Decimal
from datetime import datetime
from typing import List, Optional

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# schema
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.auth.schema.mixins.user_mixin import UserBaseMixin
from app.modules.contract.schema.mixins.under_contract_mixin import UnderContract
from app.modules.properties.schema.mixins.property_mixin import PropertyDetailsMixin
from app.modules.billing.schema.utility_schema import UtilityResponse
from app.modules.billing.schema.invoice_schema import InvoiceResponse
from app.modules.resources.schema.media_schema import MediaResponse

# models
from app.modules.contract.models.contract import Contract as ContractModel
from app.modules.contract.models.under_contract import (
    UnderContract as UnderContractModel,
)
from app.modules.contract.models.contract_type import ContractType as ContractTypeModel
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel


class ContractBase(BaseSchema):
    contract_type_id: int
    payment_type_id: int
    contract_status: Optional[ContractStatusEnum]
    contract_details: Optional[str] = None
    num_invoices: Optional[int]
    payment_amount: Optional[Decimal]
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal]
    date_signed: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    contract_info: Optional[List[UnderContract] | UnderContract] = None


class Contract(BaseSchema):
    contract_number: Optional[str] = None
    contract_id: UUID


class ContractInfoMixin(PropertyDetailsMixin, UserBaseMixin):
    @classmethod
    def get_contract_details(cls, contract_details: List[UnderContractModel]):
        result = []

        for contract_detail in contract_details:
            property_unit_assoc_query = cls.get_property_details(
                [contract_detail.properties]
            )

            result.append(
                UnderContract(
                    under_contract_id=contract_detail.under_contract_id,
                    property_unit_assoc=property_unit_assoc_query[0]
                    if len(property_unit_assoc_query) != 0
                    else None,
                    contract_number=contract_detail.contract_number,
                    contract_status=contract_detail.contract_status,
                    client_id=cls.get_user_info(contract_detail.client_representative),
                    employee_id=cls.get_user_info(
                        contract_detail.employee_representative
                    ),
                    start_date=contract_detail.start_date,
                    end_date=contract_detail.end_date,
                    next_payment_due=contract_detail.next_payment_due,
                )
            )

        return result

    @classmethod
    def get_contract_info(cls, contract_info: List[UnderContractModel]) -> List[Contract]:
        result = []

        for under_contract in contract_info:
            contract: ContractModel = under_contract.contract

            if contract:
                # Fetch related contract_type and payment_type
                contract_type: ContractTypeModel = contract.contract_type
                payment_type: PaymentTypeModel = contract.payment_type

                result.append(
                    Contract(
                        contract_id=contract.contract_id,
                        contract_number=contract.contract_number,
                        num_invoices=contract.num_invoices,
                        contract_type=contract_type.contract_type_name if contract_type else None,  # Fetch contract type name
                        payment_type=payment_type.payment_type_name if payment_type else None,  # Fetch payment type name
                        contract_status=contract.contract_status,
                        contract_details=contract.contract_details,
                        payment_amount=contract.payment_amount,
                        fee_percentage=contract.fee_percentage,
                        fee_amount=contract.fee_amount,
                        date_signed=contract.date_signed,
                        start_date=contract.start_date,
                        end_date=contract.end_date,
                        properties=contract.properties,
                        property_unit_assoc_id=under_contract.property_unit_assoc_id,
                        next_payment_due=under_contract.next_payment_due,
                    )
                )
        return result

    @classmethod
    def get_utilities_info(cls, utilities):
        return [UtilityResponse.model_validate(utility) for utility in utilities] if utilities else []

    @classmethod
    def get_invoices_info(cls, invoices):
        return [InvoiceResponse.model_validate(invoice) for invoice in invoices] if invoices else []

    @classmethod
    def get_media_info(cls, media_items):
        return [MediaResponse.model_validate(media) for media in media_items] if media_items else []
