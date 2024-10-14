from decimal import Decimal
from pydantic import BaseModel, UUID4
from typing import Optional
from pydantic import BaseModel, UUID4, Field

from app.modules.associations.enums import EntityTypeEnum

class UtilityBase(BaseModel):
    name: str
    description: Optional[str] = None

class UtilityCreateSchema(UtilityBase):
    entity_id: UUID4  # Can be contract_id or property_id
    entity_type: EntityTypeEnum  # 'contract' or 'property'
    billable_amount: float

class UtilityUpdateSchema(UtilityBase):
    pass
class UtilitySchema(UtilityBase):
    billable_assoc_id: UUID4

class UtilityResponse(BaseModel):
    utility_id: UUID4 = Field(..., description="Unique identifier for the utility")
    name: str = Field(..., max_length=128, description="Name of the utility")
    description: Optional[str] = Field(None, description="Detailed description of the utility")
    billable_amount: Decimal = Field(..., description="Amount billed for the utility")
    apply_to_units: bool = Field(..., description="Indicates if the utility applies to individual units")

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "utility_id": "1a7f9f3d-4a6c-42c7-8149-bb79db6e8f3f",
                "name": "Electricity",
                "description": "Electricity service charges for the building",
                "billable_amount": 150.75,
                "apply_to_units": True
            }
        }
