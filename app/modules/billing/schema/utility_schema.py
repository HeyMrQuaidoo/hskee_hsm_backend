from typing import Optional
from pydantic import ConfigDict

from app.modules.billing.schema.mixins.utility_mixin import UtilityBase
from app.modules.common.schema.base_schema import BaseFaker


class UtilityCreateSchema(UtilityBase):
    name: str
    description: Optional[str] = None

    # Faker attributes
    _name = BaseFaker.word()
    _description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": _name,
                "description": _description,
            }
        }
    )

class UtilityUpdateSchema(UtilityBase):
    name: Optional[str] = None
    description: Optional[str] = None

    # Faker attributes
    _name = BaseFaker.word()
    _description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": _name,
                "description": _description,
            }
        }
    )

class UtilityResponseSchema(UtilityBase):
    name: str
    description: Optional[str] = None

    # Faker attributes
    _name = BaseFaker.word()
    _description = BaseFaker.sentence()

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": _name,
                "description": _description,
            }
        }
    )