from pydantic import BaseModel, ConfigDict
from typing import Optional

# Schema
from app.modules.common.schema.base_schema import BaseFaker

# Model
from app.modules.billing.models.payment_type import PaymentType as PaymentTypeModel

# Enums
from app.modules.billing.enums.billing_enums import PaymentTypeEnum


class PaymentTypeBase(BaseModel):
    payment_type_name: PaymentTypeEnum  
    payment_type_description: Optional[str]
    payment_partitions: int


class PaymentTypeCreateSchema(PaymentTypeBase):
    # Adding BaseFaker to auto-generate example values
    _payment_type_name = BaseFaker.random_element([e.value for e in PaymentTypeEnum])
    _payment_partitions = BaseFaker.random_int(min=1, max=12)
    _payment_type_description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_type_name": _payment_type_name,
                "payment_type_description": _payment_type_description,
                "payment_partitions": _payment_partitions,
            }
        }
    )

    @classmethod
    def model_validate(cls, payment_type: PaymentTypeModel):
        return cls(
            payment_type_name=payment_type.payment_type_name,
            payment_type_description=payment_type.payment_type_description,
            payment_partitions=payment_type.payment_partitions,
        ).model_dump()


class PaymentTypeUpdateSchema(PaymentTypeBase):
    payment_type_name: Optional[PaymentTypeEnum] = None  # Enum used here
    payment_type_description: Optional[str] = None
    payment_partitions: Optional[int] = None

    # Adding BaseFaker to auto-generate example values
    _payment_type_name = BaseFaker.random_element([e.value for e in PaymentTypeEnum])
    _payment_partitions = BaseFaker.random_int(min=1, max=12)
    _payment_type_description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_type_name": _payment_type_name,
                "payment_type_description": _payment_type_description,
                "payment_partitions": _payment_partitions,
            }
        }
    )

    @classmethod
    def model_validate(cls, payment_type: PaymentTypeModel):
        return cls(
            payment_type_name=payment_type.payment_type_name,
            payment_type_description=payment_type.payment_type_description,
            payment_partitions=payment_type.payment_partitions,
        ).model_dump()


class PaymentTypeResponse(PaymentTypeBase):
    payment_type_id: int

    # Adding BaseFaker to auto-generate example values
    _payment_type_id = BaseFaker.random_int(min=1, max=100)
    _payment_type_name = BaseFaker.random_element([e.value for e in PaymentTypeEnum])
    _payment_partitions = BaseFaker.random_int(min=1, max=12)
    _payment_type_description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "payment_type_id": _payment_type_id,
                "payment_type_name": _payment_type_name,
                "payment_type_description": _payment_type_description,
                "payment_partitions": _payment_partitions,
            }
        },
        from_attributes=True
    )

    @classmethod
    def model_validate(cls, payment_type: PaymentTypeModel):
        return cls(
            payment_type_id=payment_type.payment_type_id,
            payment_type_name=payment_type.payment_type_name,
            payment_type_description=payment_type.payment_type_description,
            payment_partitions=payment_type.payment_partitions,
        ).model_dump()
