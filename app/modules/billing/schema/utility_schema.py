from typing import Optional
from uuid import UUID
from pydantic import ConfigDict

from app.modules.billing.schema.mixins.utility_mixin import UtilitiesMixin, UtilityBase


class UtilityCreateSchema(UtilityBase, UtilitiesMixin):
    utility_id: Optional[UUID] = None
    name: str
    description: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"example": UtilitiesMixin._utility_create_json}
    )


class UtilityUpdateSchema(UtilityBase, UtilitiesMixin):
    utility_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(
        json_schema_extra={"example": UtilitiesMixin._utility_update_json}
    )


class UtilitiesResponse(UtilityBase):
    utility_id: Optional[UUID] = None
    name: Optional[str] = None
    description: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)
