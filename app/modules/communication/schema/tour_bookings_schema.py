from pydantic import BaseModel, UUID4, Field, ConfigDict
from datetime import datetime
from typing import Optional

# Enums
from app.modules.communication.enums.communication_enums import TourType, TourStatus

# Models
from app.modules.communication.models.tour_bookings import TourBookings as TourModel
from app.modules.communication.schema.mixins.tour_bookings_mixin import TourInfoMixin
from app.modules.communication.schema.tour_schema import TourBase


class TourCreateSchema(TourBase, TourInfoMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={"example": TourInfoMixin._tour_create_json},
    )

    @classmethod
    def model_validate(cls, tour: TourModel):
        return cls.get_tour_info(tour).model_dump()


class TourUpdateSchema(TourBase, TourInfoMixin):
    name: Optional[str] = None
    email: Optional[str] = None
    phone_number: Optional[str] = None
    tour_type: Optional[TourType] = None
    status: Optional[TourStatus] = None
    tour_date: Optional[datetime] = None
    property_unit_assoc_id: Optional[UUID4] = None
    user_id: Optional[UUID4] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        json_schema_extra={"example": TourInfoMixin._tour_update_json},
    )

    @classmethod
    def model_validate(cls, tour: TourModel):
        return cls.get_tour_info(tour).model_dump()


class TourBookingsResponse(TourModel, TourInfoMixin):
    @classmethod
    def model_validate(cls, tour: TourModel):
        return cls.get_tour_info(tour).model_dump()
