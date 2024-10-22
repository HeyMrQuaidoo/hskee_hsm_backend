from uuid import UUID
from typing import List, Optional
from datetime import datetime

# enums
from app.modules.billing.enums.billing_enums import (
    InvoiceTypeEnum,
    PaymentStatusEnum,
)

# schemas
from app.modules.auth.schema.mixins.user_mixin import UserBase
from app.modules.common.schema.base_schema import BaseFaker, BaseSchema
from app.modules.billing.schema.mixins.invoice_mixin import InvoiceBase
from app.modules.billing.schema.mixins.payment_type_mixin import PaymentTypeBase
# from app.modules.billing.schema.mixins.transaction_type_mixin import TransactionTypeBase


# models
# from app.modules.auth.models.user import User as UserModel
from app.modules.billing.models.transaction import Transaction as TransactionModel
# from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel
# from app.modules.billing.models.transaction_type import (
#     TransactionType as TransactionTypeModel,
# )


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
    _payment_type_id = BaseFaker.random_int(min=1, max=5)
    _client_offered = str(BaseFaker.uuid4())
    _client_requested = str(BaseFaker.uuid4())
    _transaction_date = BaseFaker.date_time_this_year()
    _transaction_details = BaseFaker.text(max_nb_chars=200)
    _transaction_type = BaseFaker.random_int(min=1, max=5)
    _transaction_status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])
    _invoice_number = f"INV{BaseFaker.random_number(digits=8)}"

    _transaction_create_json = {
        "payment_type_id": "5",
        "client_offered": "7b1596ef-44bf-43e0-98cf-a1336bc39b5c",
        "client_requested": "7b1596ef-44bf-43e0-98cf-a1336bc39b5c",
        "transaction_date": _transaction_date.isoformat(),
        "transaction_details": _transaction_details,
        "transaction_type": _transaction_type,
        "transaction_status": _transaction_status,
        "invoice_number": "INV20241020135905",
        "invoice": {
                "issued_by": "7b1596ef-44bf-43e0-98cf-a1336bc39b5c",
                "issued_to": "7b1596ef-44bf-43e0-98cf-a1336bc39b5c",
                "invoice_details": BaseFaker.text(max_nb_chars=200),
                "invoice_amount": round(BaseFaker.random_number(digits=2), 2),
                "due_date": BaseFaker.future_datetime().isoformat(),
                "invoice_type": BaseFaker.random_element([e.value for e in InvoiceTypeEnum]),
                "status": BaseFaker.random_element([e.value for e in PaymentStatusEnum]),
                "invoice_items": [
                    {
                        "description": BaseFaker.sentence(),
                        "quantity": BaseFaker.random_int(min=1, max=10),
                        "unit_price": round(BaseFaker.random_number(digits=5), 2),
                        "reference_id": str(BaseFaker.uuid4()),
                    }
                ],
            }
    }

    _transaction_update_json = {
        "payment_type_id": _payment_type_id,
        "client_offered": _client_offered,
        "client_requested": _client_requested,
        "transaction_date": _transaction_date.isoformat(),
        "transaction_details": _transaction_details,
        "transaction_type": _transaction_type,
        "transaction_status": _transaction_status,
        "invoice_number": _invoice_number,
        "invoice": {
                "issued_by": "7b1596ef-44bf-43e0-98cf-a1336bc39b5c",
                "issued_to": "7b1596ef-44bf-43e0-98cf-a1336bc39b5c",
                "invoice_details": BaseFaker.text(max_nb_chars=200),
                "invoice_amount": round(BaseFaker.random_number(digits=2), 2),
                "due_date": BaseFaker.future_datetime().isoformat(),
                "invoice_type": BaseFaker.random_element([e.value for e in InvoiceTypeEnum]),
                "status": BaseFaker.random_element([e.value for e in PaymentStatusEnum]),
                "invoice_items": [
                    { 
                        "invoice_item_id": str(
                            BaseFaker.uuid4()
                        ), 
                        "description": BaseFaker.sentence(),
                        "quantity": BaseFaker.random_int(min=1, max=10),
                        "unit_price": round(BaseFaker.random_number(digits=5), 2),
                        "reference_id": str(BaseFaker.uuid4()),
                    }
                ],
            }
    }

    # @classmethod
    # def get_transaction_info(cls, transaction: TransactionModel):
    #     # payment_type: PaymentTypeModel = transaction.payment_type
    #     # transaction_type: TransactionTypeModel = transaction.transaction_types
    #     # client_offered_user: UserModel = transaction.client_offered_transaction
    #     # client_requested_user: UserModel = transaction.client_requested_transaction

    @classmethod
    def model_validate(cls, transaction: TransactionModel):
        """
        This method should only use the data in the `TransactionModel` object and should not call `get_transaction_info` again to avoid recursion.
        """
        return cls(
            transaction_id=transaction.transaction_id,
            transaction_number=transaction.transaction_number,
            transaction_details=transaction.transaction_details,
            transaction_status=transaction.transaction_status,
            payment_type_id=transaction.payment_type_id,
            transaction_type=transaction.transaction_type if transaction.transaction_type else None,
            transaction_date=transaction.transaction_date,
            invoice_number=transaction.invoice_number if transaction.invoice_number else None,
            client_offered=transaction.client_offered if transaction.client_offered else None,
            client_requested=transaction.client_requested if transaction.client_requested else None,
        )

    @classmethod
    def get_transaction_info(cls, transaction: TransactionModel) -> dict:
        """
        Return a dictionary representation of transaction info, but do not call `model_validate` inside.
        """
        return {
            "transaction_id": transaction.transaction_id,
            "transaction_number": transaction.transaction_number,
            "transaction_details": transaction.transaction_details,
            "transaction_status": transaction.transaction_status,
            "payment_type_id": transaction.payment_type_id,
            "transaction_type": transaction.transaction_type if transaction.transaction_type else None,
            "transaction_date": transaction.transaction_date,
            "invoice_number": transaction.invoice_number if transaction.invoice_number else None,
            "client_offered": transaction.client_offered if transaction.client_offered else None,
            "client_requested": transaction.client_requested if transaction.client_requested else None,
        }

    # @classmethod
    # def get_transaction_info(
    #     cls, transactions: TransactionModel | List[TransactionModel]
    # ):
    #     print(f"TRANSACTION: {transactions}")
    #     if isinstance(transactions, list):
    #         return [cls.model_validate(transaction) for transaction in transactions]
    #     return cls.model_validate(transactions)

    # @classmethod
    # def model_validate(cls, transaction: TransactionModel):
    #     return cls(
    #         transaction_id=transaction.transaction_id,
    #         transaction_number=transaction.transaction_number,
    #         transaction_details=transaction.transaction_details,
    #         transaction_status=transaction.transaction_status,
    #         payment_type=PaymentTypeBase.model_validate(transaction.payment_type),
    #         # transaction_types=TransactionTypeBase.model_validate(transaction.transaction_types),
    #         transaction_invoice=InvoiceBase.model_validate(
    #             transaction.transaction_invoice
    #         ),
    #         client_offered_transaction=UserBase.model_validate(
    #             transaction.client_offered_transaction
    #         ),
    #         client_requested_transaction=UserBase.model_validate(
    #             transaction.client_requested_transaction
    #         ),
    #     )

        # return {
        #     "transaction_id": transaction.transaction_id,
        #     "transaction_number": transaction.transaction_number,
        #     "payment_type": payment_type.payment_type_name if payment_type else None,
        #     "client_offered": {
        #         "user_id": client_offered_user.user_id,
        #         "full_name": client_offered_user.full_name,
        #     }
        #     if client_offered_user
        #     else None,
        #     "client_requested": {
        #         "user_id": client_requested_user.user_id,
        #         "full_name": client_requested_user.full_name,
        #     }
        #     if client_requested_user
        #     else None,
        #     "transaction_date": transaction.transaction_date,
        #     "transaction_details": transaction.transaction_details,
        #     "transaction_type": transaction_type.transaction_type_name
        #     if transaction_type
        #     else None,
        #     "transaction_status": transaction.transaction_status,
        #     "invoice_number": transaction.invoice_number,
        # }
