from pydantic import ConfigDict
from datetime import date, datetime

# schema imports
from app.modules.properties.schema.mixins.property_mixin_schema import PropertyDetailsMixin
from app.modules.properties.schema.mixins.property_assignment_mixin import (
    PropertyAssignmentBase,
    PropertyAssignmentMixin,
)

# models
from app.modules.properties.models.property_assignment import (
    PropertyAssignment as PropertyAssignmentModel,
)


class PropertyAssignmentCreate(PropertyAssignmentBase):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        #json_encoders={
            # date: lambda v: v.strftime("%Y-%m-%d") if v else None,
            # datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S") if v else None,
        # },
        json_schema_extra={
            "example": PropertyAssignmentMixin._property_assignment_create_json
        },
    )

    @classmethod
    def model_validate(cls, property_assignment: PropertyAssignmentModel):
        # Using the model fields directly from the property assignment instance
        return cls(
            property_unit_assoc_id=property_assignment.property_unit_assoc_id,
            user_id=property_assignment.user_id,
            assignment_type=property_assignment.assignment_type,
            date_from=property_assignment.date_from,
            date_to=property_assignment.date_to,
            notes=property_assignment.notes,
        ).model_dump()


class PropertyAssignmentUpdate(PropertyAssignmentBase):
    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        #json_encoders={
            # date: lambda v: v.strftime("%Y-%m-%d") if v else None,
            # datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S") if v else None,
        # },
        json_schema_extra={
            "example": PropertyAssignmentMixin._property_assignment_update_json
        },
    )

    @classmethod
    def model_validate(cls, property_assignment: PropertyAssignmentModel):
        return cls(
            property_unit_assoc_id=property_assignment.property_unit_assoc_id,
            user_id=property_assignment.user_id,
            assignment_type=property_assignment.assignment_type,
            date_from=property_assignment.date_from,
            date_to=property_assignment.date_to,
            notes=property_assignment.notes,
        ).model_dump()


class PropertyAssignmentResponse(PropertyAssignmentBase):
    property_info: PropertyDetailsMixin = None  # Use composition for property details

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
