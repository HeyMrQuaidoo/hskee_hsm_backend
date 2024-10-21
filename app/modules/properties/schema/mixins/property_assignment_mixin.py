from enum import Enum
from uuid import UUID
from datetime import datetime, timedelta
from typing import Any, List, Optional, Union
from pydantic import ConfigDict, model_validator

# schemas
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.auth.schema.mixins.user_mixin import UserBase
from app.modules.properties.schema.mixins.property_mixin import (
    PropertyBase,
    PropertyUnitBase,
    PropertyDetailsMixin,
    PropertyUnitAssocBase,
)

# models
from app.modules.properties.models.property_assignment import (
    PropertyAssignment as PropertyAssignmentModel,
)


class AssignmentType(str, Enum):
    """
    Enum representing types of assignments.
    """

    other = "other"
    handler = "handler"
    landlord = "landlord"
    contractor = "contractor"


class PropertyAssignmentBase(BaseSchema):
    property_unit_assoc_id: UUID
    user_id: Optional[Union[UserBase | UUID]] = None
    assignment_type: AssignmentType
    date_from: Optional[datetime]
    date_to: Optional[datetime]
    notes: Optional[str] = None
    property_info: Optional[
        Union[
            PropertyUnitAssocBase
            | PropertyUnitBase
            | PropertyBase
            | Any
            | List[PropertyUnitAssocBase]
            | List[PropertyUnitBase]
            | List[PropertyBase]
        ]
    ] = []
    # units: Optional[List[PropertyUnitBase]] = []
    # property: Optional[List[PropertyBase]] = []

    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    @model_validator(mode="after")
    def flatten_nested_info(cls, values: "PropertyAssignmentBase"):
        if not values.user_id:
            values.user_id = None

        return values


class PropertyAssignment(PropertyAssignmentBase):
    property_assignment_id: UUID


class PropertyAssignmentMixin(PropertyAssignmentBase, PropertyDetailsMixin):
    property_assignment_id: UUID

    _date_from = BaseFaker.date_time_between(start_date="-2y", end_date="now")
    _date_to = _date_from + timedelta(days=BaseFaker.random_int(min=30, max=365))
    _notes = BaseFaker.text(max_nb_chars=200)
    _assignment_type = BaseFaker.random_choices(
        ["other", "handler", "landlord", "contractor"], length=1
    )

    _property_assignment_create_json = {
        "property_unit_assoc_id": str(BaseFaker.uuid4()),
        "user_id": "e390775e-8c0d-45fd-ac4d-c7d1e75dfeff",
        "assignment_type": _assignment_type[0],
        "date_from": _date_from,
        "date_to": _date_to,
        "notes": _notes,
    }

    _property_assignment_update_json = {
        "property_unit_assoc_id": str(BaseFaker.uuid4()),
        "user_id": "e390775e-8c0d-45fd-ac4d-c7d1e75dfeff",
        "assignment_type": _assignment_type[0],
        "date_from": _date_from,
        "date_to": _date_to,
        "notes": _notes,
    }

    @classmethod
    def get_property_assignment_info(
        cls, property_assigment: Union[PropertyAssignment | List[PropertyAssignment]]
    ) -> PropertyAssignmentModel:
        result = []

        if not isinstance(property_assigment, list):
            return cls(
                property_assignment_id=property_assigment.property_assignment_id,
                property_unit_assoc_id=property_assigment.property_unit_assoc_id,
                user_id=property_assigment.user_id,
                assignment_type=property_assigment.assignment_type,
                date_from=property_assigment.date_from,
                date_to=property_assigment.date_to,
                notes=property_assigment.notes,
                property_info=cls.get_property_unit_info(property_assigment.units)
                if property_assigment.property_info.property_type
                == PropertyDetailsMixin._PROPERTY_TYPE_DEFAULT
                else cls.get_property_info(property_assigment.property),
            ).model_dump(exclude=["units", "property"])

        else:
            for property_assigment_item in property_assigment:
                result.append(
                    cls(
                        property_assignment_id=property_assigment_item.property_assignment_id,
                        property_unit_assoc_id=property_assigment_item.property_unit_assoc_id,
                        user_id=property_assigment_item.user_id,
                        assignment_type=property_assigment_item.assignment_type,
                        date_from=property_assigment_item.date_from,
                        date_to=property_assigment_item.date_to,
                        notes=property_assigment_item.notes,
                        property_info=cls.get_property_unit_info(
                            property_assigment_item.units
                        )
                        if property_assigment_item.property_info.property_type
                        == PropertyDetailsMixin._PROPERTY_TYPE_DEFAULT
                        else cls.get_property_info(property_assigment_item.property),
                    ).model_dump(exclude=["units", "property"])
                )

        return result
