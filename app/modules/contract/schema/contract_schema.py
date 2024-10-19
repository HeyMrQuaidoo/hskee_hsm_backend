from typing import Optional, List
from pydantic import ConfigDict
from decimal import Decimal
from datetime import datetime
from uuid import UUID

# Enums
from app.modules.billing.enums.billing_enums import InvoiceTypeEnum, PaymentStatusEnum
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# Schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.contract.schema.mixins.contract_mixin import (
    ContractBase,
    ContractInfoMixin,
)
from app.modules.billing.schema.mixins.utility_mixin import UtilitiesMixin

# Relationship Schemas
from app.modules.billing.schema.utility_schema import UtilityCreateSchema, UtilityResponse
from app.modules.billing.schema.invoice_schema import InvoiceCreateSchema, InvoiceResponse
from app.modules.contract.schema.under_contract_schema import UnderContractCreateSchema, UnderContractResponse
from app.modules.resources.schema.media_schema import MediaCreateSchema, MediaResponse
from app.modules.billing.schema.utility_schema import UtilityUpdateSchema
from app.modules.billing.schema.invoice_schema import InvoiceUpdateSchema
from app.modules.contract.schema.under_contract_schema import UnderContractUpdateSchema
from app.modules.resources.schema.media_schema import MediaUpdateSchema

# Models
from app.modules.contract.models.contract import Contract as ContractModel


class ContractCreateSchema(ContractBase, ContractInfoMixin, UtilitiesMixin):
    # Fields for creation
    contract_status: ContractStatusEnum
    contract_details: Optional[str] = None
    num_invoices: Optional[int] = None
    payment_amount: Decimal
    fee_percentage: Optional[Decimal] = None
    fee_amount: Decimal
    date_signed: datetime
    start_date: datetime
    end_date: datetime
    utilities: Optional[List[UtilityCreateSchema]] = None
    invoices: Optional[List[InvoiceCreateSchema]] = None
    under_contract: Optional[List[UnderContractCreateSchema]] = None
    media: Optional[List[MediaCreateSchema]] = None

    # Faker attributes
    _contract_type_id = BaseFaker.random_int(min=1, max=5)
    _payment_type_id = BaseFaker.random_int(min=1, max=5)
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_details = BaseFaker.text(max_nb_chars=200)
    _num_invoices = BaseFaker.random_int(min=1, max=10)
    _payment_amount = round(BaseFaker.random_number(digits=5), 2)
    _fee_percentage = round(BaseFaker.random_number(digits=2), 2)
    _fee_amount = round(BaseFaker.random_number(digits=4), 2)
    _date_signed = BaseFaker.date_this_year()
    _start_date = BaseFaker.date_this_year()
    _end_date = BaseFaker.future_date()

    # Faker attributes for relationships
    _utility_name = BaseFaker.word()
    _invoice_number = BaseFaker.bothify(text='INV-#####')
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_element(['image', 'video', 'document'])
    _invoice_type = BaseFaker.random_element([e.value for e in InvoiceTypeEnum])
    _status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])


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
                "date_signed": _date_signed.isoformat(),
                "start_date": _start_date.isoformat(),
                "end_date": _end_date.isoformat(),
                "utilities": [
                    {
                        "name": _utility_name,
                        # "utility_type": BaseFaker.random_element(["electricity", "water", "gas"]),
                        "description": BaseFaker.text(max_nb_chars=100),
                        # "utility_amount": round(BaseFaker.random_number(digits=4), 2),
                    }
                ],
                "invoices": [
                    {
                        # "invoice_number": _invoice_number,
                        "issued_by": str(BaseFaker.uuid4()),
                        "issued_to": str(BaseFaker.uuid4()),
                        "invoice_details": BaseFaker.text(max_nb_chars=200),
                        "due_date": BaseFaker.future_datetime().isoformat(),
                       "invoice_type": _invoice_type,
                        "status": _status,
                        "invoice_items": [
                            {
                                "description": BaseFaker.sentence(),
                                "quantity": BaseFaker.random_int(min=1, max=10),
                                "unit_price": round(BaseFaker.random_number(digits=5), 2),
                                "reference_id": str(BaseFaker.uuid4()),
                            }
                        ],
                    }
                ],
                "under_contract": [
                    {
                        "property_unit_assoc_id": str(BaseFaker.uuid4()),
                        "contract_status": _contract_status,
                        "contract_number": f"CTR-{BaseFaker.bothify(text='#####')}",
                        "client_id": str(BaseFaker.uuid4()),
                        "employee_id": str(BaseFaker.uuid4()),
                        "start_date": _start_date.isoformat(),
                        "end_date": _end_date.isoformat(),
                        "next_payment_due": BaseFaker.future_datetime().isoformat(),
                    }
                ],
                "media": [
                    {
                        "media_name": _media_name,
                        "media_type": _media_type,
                        "content_url": BaseFaker.url(),
                        "is_thumbnail": BaseFaker.boolean(),
                        "caption": BaseFaker.sentence(),
                        "description": BaseFaker.text(max_nb_chars=200),
                    }
                ],
            }
        },
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type_id=contract.contract_type_id,
            payment_type_id=contract.payment_type_id,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            utilities=cls.get_utilities_info(contract.utilities),
            invoices=[invoice.to_dict() for invoice in contract.invoices],
            under_contract=cls.get_contract_details(contract.under_contract),
            media=[media.to_dict() for media in contract.media],
        ).model_dump()


class ContractUpdateSchema(ContractBase, ContractInfoMixin, UtilitiesMixin):
    # Making all fields optional for partial updates
    contract_type_id: Optional[int] = None
    payment_type_id: Optional[int] = None
    contract_status: Optional[ContractStatusEnum] = None
    contract_details: Optional[str] = None
    num_invoices: Optional[int] = None
    payment_amount: Optional[Decimal] = None
    fee_percentage: Optional[Decimal] = None
    fee_amount: Optional[Decimal] = None
    date_signed: Optional[datetime] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    utilities: Optional[List[UtilityUpdateSchema]] = None
    invoices: Optional[List[InvoiceUpdateSchema]] = None
    under_contract: Optional[List[UnderContractUpdateSchema]] = None
    media: Optional[List[MediaUpdateSchema]] = None

    # Faker attributes
    _contract_type_id = BaseFaker.random_int(min=1, max=5)
    _payment_type_id = BaseFaker.random_int(min=1, max=5)
    _contract_status = BaseFaker.random_element([e.value for e in ContractStatusEnum])
    _contract_details = BaseFaker.text(max_nb_chars=200)
    _num_invoices = BaseFaker.random_int(min=1, max=10)
    _payment_amount = round(BaseFaker.random_number(digits=5), 2)
    _fee_percentage = round(BaseFaker.random_number(digits=2), 2)
    _fee_amount = round(BaseFaker.random_number(digits=4), 2)
    _date_signed = BaseFaker.date_this_year()
    _start_date = BaseFaker.date_this_year()
    _end_date = BaseFaker.future_date()

    # Faker attributes for relationships
    _utility_name = BaseFaker.word()
    _invoice_number = BaseFaker.bothify(text='INV-#####')
    _media_name = BaseFaker.word()
    _media_type = BaseFaker.random_element(['image', 'video', 'document'])

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
                "date_signed": _date_signed.isoformat(),
                "start_date": _start_date.isoformat(),
                "end_date": _end_date.isoformat(),
                "utilities": [
                    {
                        "utility_id": str(BaseFaker.uuid4()),
                        "name": _utility_name,
                        # "utility_type": BaseFaker.random_element(["electricity", "water", "gas"]),
                        "description": BaseFaker.text(max_nb_chars=100),
                        # "utility_amount": round(BaseFaker.random_number(digits=4), 2),
                    }
                ],
                "invoices": [
                    {
                        "invoice_id": str(BaseFaker.uuid4()),
                        # "invoice_number": _invoice_number,
                        "issued_by": str(BaseFaker.uuid4()),
                        "issued_to": str(BaseFaker.uuid4()),
                        "invoice_details": BaseFaker.text(max_nb_chars=200),
                        "due_date": BaseFaker.future_datetime().isoformat(),
                        # "date_paid": BaseFaker.date_time_this_year().isoformat(),
                        "invoice_type": BaseFaker.random_element(["standard", "credit", "debit"]),
                        "status": BaseFaker.random_element(["unpaid", "paid", "overdue"]),
                        "invoice_items": [
                            {
                                "invoice_item_id": str(BaseFaker.uuid4()),
                                "description": BaseFaker.sentence(),
                                "quantity": BaseFaker.random_int(min=1, max=10),
                                "unit_price": round(BaseFaker.random_number(digits=5), 2),
                                "total_price": round(BaseFaker.random_number(digits=6), 2),
                                "reference_id": str(BaseFaker.uuid4()),
                            },
                        ],
                    }
                ],
                "under_contract": [
                    {
                        "under_contract_id": str(BaseFaker.uuid4()),
                        "property_unit_assoc_id": str(BaseFaker.uuid4()),
                        "contract_status": _contract_status,
                        "contract_number": f"CTR-{BaseFaker.bothify(text='#####')}",
                        "client_id": str(BaseFaker.uuid4()),
                        "employee_id": str(BaseFaker.uuid4()),
                        "start_date": _start_date.isoformat(),
                        "end_date": _end_date.isoformat(),
                        "next_payment_due": BaseFaker.future_datetime().isoformat(),
                    }
                ],
                "media": [
                    {
                        "media_id": str(BaseFaker.uuid4()),
                        "media_name": _media_name,
                        "media_type": _media_type,
                        "content_url": BaseFaker.url(),
                        "is_thumbnail": BaseFaker.boolean(),
                        "caption": BaseFaker.sentence(),
                        "description": BaseFaker.text(max_nb_chars=200),
                    }
                ],
            }
        },
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type_id=contract.contract_type_id,
            payment_type_id=contract.payment_type_id,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            utilities=cls.get_utilities_info(contract.utilities),
            invoices=[invoice.to_dict() for invoice in contract.invoices],
            under_contract=cls.get_contract_details(contract.under_contract),
            media=[media.to_dict() for media in contract.media],
        ).model_dump()








class ContractResponse(ContractBase, ContractInfoMixin):
    contract_id: UUID
    contract_number: str
    utilities: Optional[List[UtilityResponse]] = None
    invoices: Optional[List[InvoiceResponse]] = None
    under_contract: Optional[List[UnderContractResponse]] = None
    media: Optional[List[MediaResponse]] = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "contract_id": str(BaseFaker.uuid4()),
                "contract_number": f"CTR-{BaseFaker.bothify(text='#####')}",
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
                "date_signed": BaseFaker.date_this_year().isoformat(),
                "start_date": BaseFaker.date_this_year().isoformat(),
                "end_date": BaseFaker.future_date().isoformat(),
                "utilities": [
                    {
                        "utility_id": str(BaseFaker.uuid4()),
                        "utility_name": BaseFaker.word(),
                        "utility_type": BaseFaker.random_element(["electricity", "water", "gas"]),
                        "utility_description": BaseFaker.text(max_nb_chars=100),
                        "utility_amount": round(BaseFaker.random_number(digits=4), 2),
                    }
                ],
                "invoices": [
                    {
                        "invoice_id": str(BaseFaker.uuid4()),
                        "invoice_number": f"INV{BaseFaker.random_number(digits=8)}",
                        "issued_by": str(BaseFaker.uuid4()),
                        "issued_to": str(BaseFaker.uuid4()),
                        "invoice_details": BaseFaker.text(max_nb_chars=200),
                        "due_date": BaseFaker.future_datetime().isoformat(),
                        "date_paid": BaseFaker.date_time_this_year().isoformat(),
                        "invoice_type": BaseFaker.random_element([e.value for e in InvoiceTypeEnum]),
                        "status": BaseFaker.random_element([e.value for e in PaymentStatusEnum]),
                        "invoice_amount": round(BaseFaker.random_number(digits=5), 2),
                        "invoice_items": [
                            {
                                "invoice_item_id": str(BaseFaker.uuid4()),
                                "description": BaseFaker.sentence(),
                                "quantity": BaseFaker.random_int(min=1, max=10),
                                "unit_price": round(BaseFaker.random_number(digits=5), 2),
                                "total_price": round(BaseFaker.random_number(digits=6), 2),
                                "reference_id": str(BaseFaker.uuid4()),
                            },
                        ],
                    }
                ],
                "under_contract": [
                    {
                        "under_contract_id": str(BaseFaker.uuid4()),
                        "property_unit_assoc_id": str(BaseFaker.uuid4()),
                        "contract_status": BaseFaker.random_element([e.value for e in ContractStatusEnum]),
                        "contract_number": f"CTR-{BaseFaker.bothify(text='#####')}",
                        "client_id": str(BaseFaker.uuid4()),
                        "employee_id": str(BaseFaker.uuid4()),
                        "start_date": BaseFaker.date_this_year().isoformat(),
                        "end_date": BaseFaker.future_date().isoformat(),
                        "next_payment_due": BaseFaker.future_datetime().isoformat(),
                    }
                ],
                "media": [
                    {
                        "media_id": str(BaseFaker.uuid4()),
                        "media_name": BaseFaker.word(),
                        "media_type": BaseFaker.random_element(["image", "video", "document"]),
                        "content_url": BaseFaker.url(),
                        "is_thumbnail": BaseFaker.boolean(),
                        "caption": BaseFaker.sentence(),
                        "description": BaseFaker.text(max_nb_chars=200),
                    }
                ],
            }
        },
    )

    @classmethod
    def model_validate(cls, contract: ContractModel):
        return cls(
            contract_id=contract.contract_id,
            contract_number=contract.contract_number,
            contract_type_id=contract.contract_type_id,
            payment_type_id=contract.payment_type_id,
            contract_status=contract.contract_status,
            contract_details=contract.contract_details,
            num_invoices=contract.num_invoices,
            payment_amount=contract.payment_amount,
            fee_percentage=contract.fee_percentage,
            fee_amount=contract.fee_amount,
            date_signed=contract.date_signed,
            start_date=contract.start_date,
            end_date=contract.end_date,
            utilities=cls.get_utilities_info(contract.utilities),
            invoices=cls.get_invoices_info(contract.invoices),
            under_contract=cls.get_contract_details(contract.under_contract),
            media=cls.get_media_info(contract.media),
        ).model_dump()

