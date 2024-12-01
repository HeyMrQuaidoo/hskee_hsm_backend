from pydantic import UUID4, ConfigDict
from datetime import datetime
from typing import Optional

# Mixins
from app.modules.auth.schema.mixins.user_interactions_mixin import (
    UserInteractionsBase,
    UserInteractionsInfoMixin,
)

# Models
from app.modules.auth.models.user_interactions import (
    UserInteractions as UserInteractionsModel,
)


class UserInteractionsCreateSchema(UserInteractionsBase, UserInteractionsInfoMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": UserInteractionsInfoMixin._user_interactions_create_json
        },
    )

    @classmethod
    def model_validate(cls, interaction: UserInteractionsModel):
        return cls.get_user_interactions_info(interaction)


class UserInteractionsUpdateSchema(UserInteractionsBase, UserInteractionsInfoMixin):
    user_id: Optional[UUID4] = None
    employee_id: Optional[UUID4] = None
    property_unit_assoc_id: Optional[UUID4] = None
    contact_time: Optional[datetime] = None
    contact_details: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": UserInteractionsInfoMixin._user_interactions_update_json
        },
    )

    @classmethod
    def model_validate(cls, interaction: UserInteractionsModel):
        return cls.get_user_interactions_info(interaction)


class UserInteractionsResponse(UserInteractionsModel, UserInteractionsInfoMixin):
    @classmethod
    def model_validate(cls, interaction: UserInteractionsModel):
        return cls.get_user_interactions_info(interaction)
