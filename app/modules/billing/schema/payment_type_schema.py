from pydantic import BaseModel, ConfigDict
from typing import Optional

class PaymentTypeBase(BaseModel):
    payment_type: str
    payment_type_description: Optional[str]
    payment_partitions: int

    model_config = ConfigDict(
        # orm_mode=True,
        from_attributes=True,
        json_schema_extra={
            "example": {
                "payment_type": "Annually",
                "payment_type_description": "Payment made via credit card.",
                "payment_partitions": "1"
            }
        }
    )

class PaymentTypeCreateSchema(PaymentTypeBase):
    pass

class PaymentTypeUpdateSchema(PaymentTypeBase):
    payment_type: Optional[str] = None
    payment_type_description: Optional[str] = None

class PaymentTypeResponse(PaymentTypeBase):
    payment_type_id: int

    model_config = ConfigDict(
        # orm_mode=True,
        json_schema_extra={
            "example": {
                "payment_type_id": 1,
                "payment_type": "Credit Card",
                "payment_type_description": "Payment made via credit card."
            }
        }
    )
