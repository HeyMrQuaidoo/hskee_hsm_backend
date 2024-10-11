from pydantic import BaseModel, UUID4
from typing import Optional

class UtilityBase(BaseModel):
    name: str
    description: Optional[str] = None

class UtilityCreateSchema(UtilityBase):
    pass

class UtilityUpdateSchema(UtilityBase):
    pass

class UtilitySchema(UtilityBase):
    billable_assoc_id: UUID4
