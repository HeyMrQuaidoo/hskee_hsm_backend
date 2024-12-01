from uuid import UUID
from datetime import datetime
from pydantic import ConfigDict
from typing import Optional, List, Union

# enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum, InvoiceTypeEnum

# schema
from app.modules.auth.schema.mixins.user_mixin import UserBase, UserBaseMixin
from app.modules.billing.schema.mixins.invoice_mixin import (
    Invoice,
    InvoiceBase,
    InvoiceInfoMixin,
)
from app.modules.billing.schema.mixins.invoice_item_mixin import (
    InvoiceItem,
    InvoiceItemBase,
)

# models
from app.modules.billing.models.invoice import Invoice as InvoiceModel


class InvoiceCreateSchema(Invoice, InvoiceInfoMixin, UserBaseMixin):
    invoice_id: Optional[UUID] = None
    invoice_number: Optional[str] = None
    invoice_items: Optional[List[InvoiceItemBase]] = []

    model_config = ConfigDict(
        json_schema_extra={"example": InvoiceInfoMixin._invoice_create_json},
    )

    @classmethod
    def model_validate(cls, invoice: InvoiceModel):
        return cls(
            invoice_id=invoice.invoice_id,
            invoice_number=invoice.invoice_number,
            invoice_amount=invoice.invoice_amount,
            invoice_details=invoice.invoice_details,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            invoice_type=invoice.invoice_type,
            status=invoice.status,
            transaction_number=invoice.transaction_number,
            issued_by=cls.get_user_info(invoice.issued_by_user),
            issued_to=cls.get_user_info(invoice.issued_to_user),
            invoice_items=[
                InvoiceItemBase.model_validate(item) for item in invoice.invoice_items
            ],
        ).model_dump()


class InvoiceUpdateSchema(Invoice, InvoiceInfoMixin, UserBaseMixin):
    issued_by: Optional[Union[UUID | UserBase]] = None
    issued_to: Optional[Union[UUID | UserBase]] = None
    invoice_details: Optional[str] = None
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    invoice_type: Optional[InvoiceTypeEnum] = None
    status: Optional[PaymentStatusEnum] = None
    invoice_amount: Optional[float] = None
    invoice_id: Optional[UUID] = None
    invoice_number: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"example": InvoiceInfoMixin._invoice_update_json},
    )

    @classmethod
    def model_validate(cls, invoice: InvoiceModel):
        return cls(
            invoice_id=invoice.invoice_id,
            invoice_number=invoice.invoice_number,
            invoice_amount=invoice.invoice_amount,
            invoice_details=invoice.invoice_details,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            invoice_type=invoice.invoice_type,
            status=invoice.status,
            transaction_number=invoice.transaction_number,
            issued_by=cls.get_user_info(invoice.issued_by_user),
            issued_to=cls.get_user_info(invoice.issued_to_user),
            invoice_items=[
                InvoiceItemBase.model_validate(item) for item in invoice.invoice_items
            ],
            # transaction=TransactionBase.model_validate(invoice.transaction),
            # contracts=[ContractBase.model_validate(contract) for contract in invoice.contracts]
        ).model_dump()


class InvoiceResponse(Invoice, InvoiceInfoMixin, UserBaseMixin):
    invoice_id: Optional[UUID] = None
    invoice_number: Optional[str]=None
    invoice_amount: float
    date_paid: Optional[datetime] = None
    invoice_items: Optional[List[InvoiceItem]] = []

    model_config = ConfigDict(
        json_schema_extra={"example": InvoiceInfoMixin._invoice_create_json},
    )

    @classmethod
    def model_validate(cls, invoice: InvoiceModel):
        return cls(
            invoice_id=invoice.invoice_id,
            invoice_number=invoice.invoice_number,
            invoice_amount=invoice.invoice_amount,
            invoice_details=invoice.invoice_details,
            due_date=invoice.due_date,
            date_paid=invoice.date_paid,
            invoice_type=invoice.invoice_type,
            status=invoice.status,
            transaction_number=invoice.transaction_number,
            issued_by=cls.get_user_info(invoice.issued_by_user),
            issued_to=cls.get_user_info(invoice.issued_to_user),
            invoice_items=[
                InvoiceItemBase.model_validate(item) for item in invoice.invoice_items
            ],
            # transaction=TransactionBase.model_validate(invoice.transaction),
            # contracts=[ContractBase.model_validate(contract) for contract in invoice.contracts]
        ).model_dump()
