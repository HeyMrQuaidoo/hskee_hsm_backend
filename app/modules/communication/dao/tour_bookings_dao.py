from datetime import datetime
from typing import Optional, List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import or_
from sqlalchemy import String

# DAO
from app.core.response import DAOResponse
from app.modules.common.dao.base_dao import BaseDAO

# Models
from app.modules.communication.models.tour_bookings import TourBookings
from app.modules.communication.enums.communication_enums import TourType, TourStatus

# Core
from app.core.errors import CustomException, IntegrityError
from pydantic import UUID4


class TourDAO(BaseDAO[TourBookings]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = TourBookings

        # Initializing DAOs for related entities if necessary
        self.detail_mappings = {
            # "user": UserDAO(),
            # "property": PropertyDAO(),
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="tour_booking_id",
        )

    async def get_tours(
        self,
        db_session: AsyncSession,
        user_id: Optional[UUID4] = None,
        email: Optional[str] = None,
        name: Optional[str] = None,
        phone_number: Optional[str] = None,
        status: Optional[TourStatus] = None,
        tour_type: Optional[TourType] = None,
        date_gte: Optional[datetime] = None,
        date_lte: Optional[datetime] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            query = select(self.model)

            filter_conditions = {
                "user_id": self.model.user_id == user_id if user_id else None,
                "email": self.model.email.ilike(f"%{email}%") if email else None,
                "name": self.model.name.ilike(f"%{name}%") if name else None,
                "phone_number": self.model.phone_number.ilike(f"%{phone_number}%") if phone_number else None,
                "status": self.model.status == status if status else None,
                "tour_type": self.model.tour_type == tour_type if tour_type else None,
                "date_gte": self.model.tour_date >= date_gte if date_gte else None,
                "date_lte": self.model.tour_date <= date_lte if date_lte else None,
            }

            filters = [condition for condition in filter_conditions.values() if condition is not None]
            if filters:
                query = query.where(*filters)

            query = query.order_by(self.model.tour_date.desc())

            total_query = select(func.count()).select_from(query.subquery())
            query = query.limit(limit).offset(offset)

            # Executing queries
            result = await db_session.execute(query)
            tours = result.scalars().all()

            total_items_result = await db_session.execute(total_query)
            total_count = total_items_result.scalar()

            meta = {
                "total_items": total_count,
                "limit": limit,
                "offset": offset,
            }

            return DAOResponse(success=True, data=tours, meta=meta)
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise CustomException(str(e))
