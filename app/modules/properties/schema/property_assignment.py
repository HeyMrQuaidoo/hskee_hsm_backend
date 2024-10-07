from uuid import uuid4
from pydantic import UUID4, ConfigDict
from datetime import date, datetime, timedelta

# schema
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.properties.schema.mixins.property_assignment_mixin import (
    PropertyAssignmentBase,
)
from app.modules.properties.schema.mixins.property_mixin import (
    PropertyDetailsMixin,
)

# models
from app.modules.properties.models.property_assignment import (
    PropertyAssignment as PropertyAssignmentModel,
)


class PropertyAssignmentCreate(PropertyAssignmentBase):
    _date_from = BaseFaker.date_time_between(
        start_date="-2y", end_date="now"
    )  # Generate random datetime
    _date_to = _date_from + timedelta(
        days=BaseFaker.random_int(min=30, max=365)
    )  # Add random days to _date_from
    _notes = BaseFaker.text(max_nb_chars=200)
    _assignment_type = BaseFaker.random_choices(
        ["other", "handler", "landlord", "contractor"], length=1
    )

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={
            date: lambda v: v.strftime("%Y-%m-%d") if v else None,
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S") if v else None,
        },
        json_schema_extra={
            "example": {
                "property_unit_assoc_id": str(uuid4()), # Random UUID for property unit
                "user_id": "e390775e-8c0d-45fd-ac4d-c7d1e75dfeff",  # Random UUID for user
                "assignment_type": _assignment_type[0],  # Random assignment type
                "date_from": _date_from,  # Random start date
                "date_to": _date_to,  # Random end date
                "notes": _notes,  # Random notes
            }
        },
    )

    @classmethod
    def model_validate(cls, property_assignment: PropertyAssignmentModel):
        return cls(
            property_unit_assoc_id=property_assignment.property_assignment_id,
            user_id=property_assignment.user_id,
            assignment_type=property_assignment.assignment_type,
            date_from=property_assignment.date_from,
            date_to=property_assignment.date_to,
            notes=property_assignment.notes,
        ).model_dump()


class PropertyAssignmentUpdate(PropertyAssignmentBase):
    _date_from = BaseFaker.date_time_between(
        start_date="-2y", end_date="now"
    )  # Generate random datetime
    _date_to = _date_from + timedelta(
        days=BaseFaker.random_int(min=30, max=365)
    )  # Add random days to _date_from
    _notes = BaseFaker.text(max_nb_chars=200)
    _assignment_type = BaseFaker.random_choices(
        ["other", "handler", "landlord", "contractor"], length=1
    )

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        json_encoders={
            date: lambda v: v.strftime("%Y-%m-%d") if v else None,
            datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S") if v else None,
        },
        json_schema_extra={
            "example": {
                "property_unit_assoc_id": str(uuid4()), # Random UUID for property unit
                "user_id": "e390775e-8c0d-45fd-ac4d-c7d1e75dfeff",  # Random UUID for user
                "assignment_type": _assignment_type[0],  # Random assignment type
                "date_from": _date_from,  # Random start date
                "date_to": _date_to,  # Random end date
                "notes": _notes,  # Random notes
            }
        },
    )

    @classmethod
    def model_validate(cls, property_assignment: PropertyAssignmentModel):
        return cls(
            property_unit_assoc_id=property_assignment.property_assignment_id,
            user_id=property_assignment.user_id,
            assignment_type=property_assignment.assignment_type,
            date_from=property_assignment.date_from,
            date_to=property_assignment.date_to,
            notes=property_assignment.notes,
        ).model_dump()


class PropertyAssignmentResponse(PropertyAssignmentBase, PropertyDetailsMixin):
    @classmethod
    def model_validate(cls, property_assignment: PropertyAssignmentModel):
        return cls(
            property_assignment_id=property_assignment.property_assignment_id,
            property_unit_assoc_id=property_assignment.property_unit_assoc_id,
            user_id=property_assignment.user_id,
            assignment_type=property_assignment.assignment_type,
            date_from=property_assignment.date_from,
            date_to=property_assignment.date_to,
            notes=property_assignment.notes,
            property_info=PropertyDetailsMixin.get_property_details(
                property_assignment.property_info
            ),
        ).model_dump()
