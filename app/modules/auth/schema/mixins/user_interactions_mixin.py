from pydantic import BaseModel, UUID4
from datetime import datetime

# Base Faker
from app.modules.common.schema.base_schema import BaseFaker

# Models
from app.modules.auth.models.user_interactions import UserInteractions as UserInteractionsModel

class UserInteractionsBase(BaseModel):
    user_id: UUID4
    employee_id: UUID4
    property_unit_assoc_id: UUID4
    contact_time: datetime
    contact_details: str

    class Config:
        from_attributes = True


class UserInteractions(UserInteractionsBase):
    user_interaction_id: UUID4


# Step 2: Add Schema Mixin with BaseFaker Examples

class UserInteractionsInfoMixin:
    _user_id = BaseFaker.uuid4()
    _employee_id = BaseFaker.uuid4()
    _property_unit_assoc_id = BaseFaker.uuid4()
    _contact_time = BaseFaker.past_datetime()
    _contact_details = BaseFaker.text(max_nb_chars=200)

    _user_interactions_create_json = {
        "user_id": _user_id,
        "employee_id": _employee_id,
        "property_unit_assoc_id": _property_unit_assoc_id,
        "contact_time": _contact_time.isoformat(),
        "contact_details": _contact_details,
    }

    _user_interactions_update_json = {
        "user_id": _user_id,
        "employee_id": _employee_id,
        "property_unit_assoc_id": _property_unit_assoc_id,
        "contact_time": _contact_time.isoformat(),
        "contact_details": _contact_details,
    }

    @classmethod
    def get_user_interactions_info(cls, interaction: UserInteractionsModel) -> UserInteractions:
        return UserInteractions(
            user_interaction_id=interaction.user_interaction_id,
            user_id=interaction.user_id,
            employee_id=interaction.employee_id,
            property_unit_assoc_id=interaction.property_unit_assoc_id,
            contact_time=interaction.contact_time,
            contact_details=interaction.contact_details,
        )
