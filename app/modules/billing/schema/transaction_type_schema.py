from pydantic import BaseModel, ConfigDict
from typing import Optional

class TransactionTypeBase(BaseModel):
    transaction_type_name: str
    transaction_type_description: Optional[str]

    model_config = ConfigDict(
        # orm_mode=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "transaction_type_name": "Refund",
                "transaction_type_description": "Transaction for refunding payments."
            }
        }
    )

class TransactionTypeCreateSchema(TransactionTypeBase):
    pass

class TransactionTypeUpdateSchema(TransactionTypeBase):
    transaction_type_name: Optional[str] = None
    transaction_type_description: Optional[str] = None

class TransactionTypeResponse(TransactionTypeBase):
    transaction_type_id: int

    model_config = ConfigDict(
        # orm_mode=True,
        json_schema_extra={
            "example": {
                "transaction_type_id": 1,
                "transaction_type_name": "Refund",
                "transaction_type_description": "Transaction for refunding payments."
            }
        }
    )
