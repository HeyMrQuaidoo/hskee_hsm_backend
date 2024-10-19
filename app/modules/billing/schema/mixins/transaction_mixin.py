from uuid import UUID
from datetime import datetime
from typing import Optional

# Enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum

# Base schema
from app.modules.common.schema.base_schema import BaseSchema

# Models
from app.modules.billing.models.transaction import Transaction as TransactionModel
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel
from app.modules.billing.models.transaction_type import TransactionType as TransactionTypeModel
from app.modules.auth.models.user import User as UserModel

class TransactionBase(BaseSchema):
    payment_type_id: int
    client_offered: UUID
    client_requested: UUID
    transaction_date: datetime
    transaction_details: str
    transaction_type: int
    transaction_status: PaymentStatusEnum
    invoice_number: Optional[str] = None

class Transaction(BaseSchema):
    transaction_id: UUID
    transaction_number: str

class TransactionInfoMixin:
    @classmethod
    def get_transaction_info(cls, transaction: TransactionModel):
        payment_type: PaymentTypeModel = transaction.payment_type
        transaction_type: TransactionTypeModel = transaction.transaction_types
        client_offered_user: UserModel = transaction.client_offered_transaction
        client_requested_user: UserModel = transaction.client_requested_transaction

        return {
            "transaction_id": transaction.transaction_id,
            "transaction_number": transaction.transaction_number,
            "payment_type": payment_type.payment_type_name if payment_type else None,
            "client_offered": {
                "user_id": client_offered_user.user_id,
                "full_name": client_offered_user.full_name,
            } if client_offered_user else None,
            "client_requested": {
                "user_id": client_requested_user.user_id,
                "full_name": client_requested_user.full_name,
            } if client_requested_user else None,
            "transaction_date": transaction.transaction_date,
            "transaction_details": transaction.transaction_details,
            "transaction_type": transaction_type.transaction_type_name if transaction_type else None,
            "transaction_status": transaction.transaction_status,
            "invoice_number": transaction.invoice_number,
        }
