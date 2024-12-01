from pydantic import BaseModel, UUID4
from datetime import datetime
from typing import Optional

# Enums
from app.modules.communication.enums.communication_enums import TourType, TourStatus

# Base Faker for generating example data
from app.modules.common.schema.base_schema import BaseFaker

# Models
from app.modules.communication.models.tour_bookings import TourBookings as TourModel


class TourBase(BaseModel):
    name: str
    email: str
    phone_number: str
    tour_type: TourType
    status: TourStatus
    tour_date: datetime
    property_unit_assoc_id: UUID4
    user_id: Optional[UUID4] = None

    class Config:
        from_attributes = True
        use_enum_values = True


class TourBookings(TourBase):
    tour_booking_id: UUID4


# 2. Add Schema Mixin with BaseFaker Examples


class TourInfoMixin:
    # BaseFaker attributes for generating example data
    _name = BaseFaker.name()
    _email = BaseFaker.email()
    _phone_number = BaseFaker.phone_number()
    _tour_type = BaseFaker.random_choices(["in_person", "video_chat"], length=1)
    _status = BaseFaker.random_choices(["incoming", "cancelled", "completed"], length=1)
    _tour_date = BaseFaker.future_datetime()
    _property_unit_assoc_id = BaseFaker.uuid4()
    _user_id = BaseFaker.uuid4()

    _tour_create_json = {
        "name": _name,
        "email": _email,
        "phone_number": _phone_number,
        "tour_type": _tour_type[0],
        "status": _status[0],
        "tour_date": _tour_date.isoformat(),
        "property_unit_assoc_id": _property_unit_assoc_id,
        "user_id": _user_id,
    }

    _tour_update_json = {
        "name": _name,
        "email": _email,
        "phone_number": _phone_number,
        "tour_type": _tour_type[0],
        "status": _status[0],
        "tour_date": _tour_date.isoformat(),
        "property_unit_assoc_id": _property_unit_assoc_id,
        "user_id": _user_id,
    }

    @classmethod
    def get_tour_info(cls, tour: TourModel) -> TourBookings:
        return TourBookings(
            tour_booking_id=tour.tour_booking_id,
            name=tour.name,
            email=tour.email,
            phone_number=tour.phone_number,
            tour_type=tour.tour_type,
            status=tour.status,
            tour_date=tour.tour_date,
            property_unit_assoc_id=tour.property_unit_assoc_id,
            user_id=tour.user_id,
        )
