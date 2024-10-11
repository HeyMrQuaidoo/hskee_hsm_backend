from pydantic import BaseModel, UUID4
from typing import Optional
from datetime import datetime
from app.modules.billing.enums.billing_enums import BillableTypeEnum
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


class EntityBillableBase(BaseModel):
    entity_id: UUID4
    entity_type: EntityTypeEnum
    billable_id: UUID4
    billable_type: BillableTypeEnum
    billable_amount: float
    apply_to_units: bool
    start_period: Optional[datetime] = None
    end_period: Optional[datetime] = None


class EntityBillableSchema(EntityBillableBase):
    entity_billable_id: UUID4

    class Config:
        orm_mode = True


class EntityBillableUpdateSchema(BaseModel):
    billable_amount: Optional[float] = None
    apply_to_units: Optional[bool] = None
    start_period: Optional[datetime] = None
    end_period: Optional[datetime] = None

    class Config:
        orm_mode = True
