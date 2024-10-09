from pydantic import BaseModel, UUID4
from typing import Optional

class AmenityBase(BaseModel):
    amenity_name: str
    amenity_short_name: str
    description: Optional[str] = None

class AmenityCreateSchema(AmenityBase):
    pass

class AmenityUpdateSchema(AmenityBase):
    pass

class AmenitySchema(AmenityBase):
    amenity_id: UUID4
