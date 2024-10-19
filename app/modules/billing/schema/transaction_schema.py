from datetime import datetime
from typing import Optional
from pydantic import ConfigDict
from sqlalchemy import UUID

# Enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum

# Base Faker
from app.modules.common.schema.base_schema import BaseFaker

# Mixins
from app.modules.billing.schema.mixins.transaction_mixin import (
    TransactionBase,
    TransactionInfoMixin,
    Transaction,
)

# Models
from app.modules.billing.models.transaction import Transaction as TransactionModel

class TransactionCreateSchema(TransactionBase):
    # Faker attributes for example data
    _payment_type_id = BaseFaker.random_int(min=1, max=5)
    _client_offered = str(BaseFaker.uuid4())
    _client_requested = str(BaseFaker.uuid4())
    _transaction_date = BaseFaker.date_time_this_year()
    _transaction_details = BaseFaker.text(max_nb_chars=200)
    _transaction_type = BaseFaker.random_int(min=1, max=5)
    _transaction_status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])
    _invoice_number = f"INV{BaseFaker.random_number(digits=8)}"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_type_id": _payment_type_id,
                "client_offered": _client_offered,
                "client_requested": _client_requested,
                "transaction_date": _transaction_date.isoformat(),
                "transaction_details": _transaction_details,
                "transaction_type": _transaction_type,
                "transaction_status": _transaction_status,
                "invoice_number": _invoice_number,
            }
        },
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

    # Faker attributes for example data
    _payment_type_id = BaseFaker.random_int(min=1, max=5)
    _client_offered = str(BaseFaker.uuid4())
    _client_requested = str(BaseFaker.uuid4())
    _transaction_date = BaseFaker.date_time_this_year()
    _transaction_details = BaseFaker.text(max_nb_chars=200)
    _transaction_type = BaseFaker.random_int(min=1, max=5)
    _transaction_status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])
    _invoice_number = f"INV{BaseFaker.random_number(digits=8)}"

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_type_id": _payment_type_id,
                "client_offered": _client_offered,
                "client_requested": _client_requested,
                "transaction_date": _transaction_date.isoformat(),
                "transaction_details": _transaction_details,
                "transaction_type": _transaction_type,
                "transaction_status": _transaction_status,
                "invoice_number": _invoice_number,
            }
        },
    )

class TransactionResponse(TransactionBase, TransactionInfoMixin):
    transaction_id: UUID
    transaction_number: str

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_id": str(BaseFaker.uuid4()),
                "transaction_number": f"TRN{BaseFaker.random_number(digits=8)}",
                "payment_type_id": BaseFaker.random_int(min=1, max=5),
                "client_offered": str(BaseFaker.uuid4()),
                "client_requested": str(BaseFaker.uuid4()),
                "transaction_date": BaseFaker.date_time_this_year().isoformat(),
                "transaction_details": BaseFaker.text(max_nb_chars=200),
                "transaction_type": BaseFaker.random_int(min=1, max=5),
                "transaction_status": BaseFaker.random_element(
                    [e.value for e in PaymentStatusEnum]
                ),
                "invoice_number": f"INV{BaseFaker.random_number(digits=8)}",
            }
        },
    )

    @classmethod
    def model_validate(cls, transaction: TransactionModel):
        transaction_info = cls.get_transaction_info(transaction)
        return cls(**transaction_info)
