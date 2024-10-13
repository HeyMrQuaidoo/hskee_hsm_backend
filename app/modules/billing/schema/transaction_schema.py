from pydantic import UUID4
from datetime import datetime

from app.modules.common.schema.base_schema import BaseSchema


class TransactionBase(BaseSchema):
    # transaction_id: UUID4
    # transaction_number: str
    payment_type_id: int
    client_offered: UUID4
    client_requested: UUID4
    transaction_date: datetime
    transaction_details: str
    transaction_type: int
    transaction_status: str
    invoice_number: str


class Transaction(TransactionBase):
    transaction_id: UUID4
    transaction_number: str
