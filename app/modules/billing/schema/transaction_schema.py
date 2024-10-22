from uuid import UUID
from typing import Optional
from datetime import datetime
from pydantic import ConfigDict

# enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum

# mixins
from app.modules.billing.schema.mixins.invoice_mixin import InvoiceBase
from app.modules.billing.schema.mixins.transaction_mixin import (
    TransactionBase,
    TransactionInfoMixin,
)

# models
from app.modules.billing.models.transaction import Transaction as TransactionModel


class TransactionCreateSchema(TransactionBase, TransactionInfoMixin):
    invoice: Optional[InvoiceBase] = None
    model_config = ConfigDict(
        json_schema_extra={"example": TransactionInfoMixin._transaction_create_json},
    )


class TransactionUpdateSchema(TransactionBase):
    payment_type_id: Optional[int] = None
    client_offered: Optional[UUID] = None
    client_requested: Optional[UUID] = None
    transaction_date: Optional[datetime] = None
    transaction_details: Optional[str] = None
    transaction_type: Optional[int] = None
    transaction_status: Optional[PaymentStatusEnum] = None
    invoice_number: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"example": TransactionInfoMixin._transaction_update_json},
    )


class TransactionResponse(TransactionBase, TransactionInfoMixin):
    transaction_id: UUID
    transaction_number: str

    @classmethod
    def model_validate(cls, transaction: TransactionModel):
        return cls.get_transaction_info(transaction)
        # return cls(**transaction_info).model_dump()
