from pydantic import BaseModel, ConfigDict
from typing import Optional

# Schema
from app.modules.common.schema.base_schema import BaseFaker 

# Model
from app.modules.billing.models.transaction_type import TransactionType as TransactionTypeModel  

# Enum
from app.modules.billing.enums.billing_enums import TransactionTypeEnum  


class TransactionTypeBase(BaseModel):
    transaction_type_name: TransactionTypeEnum  
    transaction_type_description: Optional[str]


class TransactionTypeCreateSchema(TransactionTypeBase):
    # Adding BaseFaker to auto-generate example values
    _transaction_type_name = BaseFaker.random_element([e.value for e in TransactionTypeEnum])
    _transaction_type_description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_type_name": _transaction_type_name,
                "transaction_type_description": _transaction_type_description,
            }
        }
    )

    @classmethod
    def model_validate(cls, transaction_type: TransactionTypeModel):
        return cls(
            transaction_type_name=transaction_type.transaction_type_name,
            transaction_type_description=transaction_type.transaction_type_description,
        ).model_dump()


class TransactionTypeUpdateSchema(TransactionTypeBase):
    transaction_type_name: Optional[TransactionTypeEnum] = None  # Enum used here
    transaction_type_description: Optional[str] = None

    # Adding BaseFaker to auto-generate example values
    _transaction_type_name = BaseFaker.random_element([e.value for e in TransactionTypeEnum])
    _transaction_type_description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_type_name": _transaction_type_name,
                "transaction_type_description": _transaction_type_description,
            }
        }
    )

    @classmethod
    def model_validate(cls, transaction_type: TransactionTypeModel):
        return cls(
            transaction_type_name=transaction_type.transaction_type_name,
            transaction_type_description=transaction_type.transaction_type_description,
        ).model_dump()


class TransactionTypeResponse(TransactionTypeBase):
    transaction_type_id: int

    # Adding BaseFaker to auto-generate example values
    _transaction_type_id = BaseFaker.random_int(min=1, max=100)
    _transaction_type_name = BaseFaker.random_element([e.value for e in TransactionTypeEnum])
    _transaction_type_description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "transaction_type_id": _transaction_type_id,
                "transaction_type_name": _transaction_type_name,
                "transaction_type_description": _transaction_type_description,
            }
        },
        from_attributes=True
    )

    @classmethod
    def model_validate(cls, transaction_type: TransactionTypeModel):
        return cls(
            transaction_type_id=transaction_type.transaction_type_id,
            transaction_type_name=transaction_type.transaction_type_name,
            transaction_type_description=transaction_type.transaction_type_description,
        ).model_dump()
