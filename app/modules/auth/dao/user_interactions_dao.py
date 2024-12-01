from datetime import datetime
from typing import Optional, List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.core.response import DAOResponse
from app.modules.common.dao.base_dao import BaseDAO

# Models
from app.modules.auth.models.user_interactions import UserInteractions

# Core
from app.core.errors import CustomException, IntegrityError
from pydantic import UUID4


class UserInteractionsDAO(BaseDAO[UserInteractions]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = UserInteractions

        # Initializing DAOs for related entities if necessary
        self.detail_mappings = {
            # "user": UserDAO(),
            # "employee": UserDAO(),
            # "property": PropertyDAO(),
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="user_interaction_id",
        )

    async def get_interactions(
        self,
        db_session: AsyncSession,
        user_id: Optional[UUID4] = None,
        employee_id: Optional[UUID4] = None,
        property_unit_assoc_id: Optional[UUID4] = None,
        date_gte: Optional[datetime] = None,
        date_lte: Optional[datetime] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            query = select(self.model)

            filter_conditions = {
                "user_id": self.model.user_id == user_id if user_id else None,
                "employee_id": self.model.employee_id == employee_id
                if employee_id
                else None,
                "property_unit_assoc_id": self.model.property_unit_assoc_id
                == property_unit_assoc_id
                if property_unit_assoc_id
                else None,
                "date_gte": self.model.contact_time >= date_gte if date_gte else None,
                "date_lte": self.model.contact_time <= date_lte if date_lte else None,
            }

            filters = [
                condition
                for condition in filter_conditions.values()
                if condition is not None
            ]
            if filters:
                query = query.where(*filters)

            # Applying ordering
            query = query.order_by(self.model.contact_time.desc())

            total_query = select(func.count()).select_from(query.subquery())
            query = query.limit(limit).offset(offset)

            # Executing queries
            result = await db_session.execute(query)
            interactions = result.scalars().all()

            total_items_result = await db_session.execute(total_query)
            total_count = total_items_result.scalar()

            meta = {
                "total_items": total_count,
                "limit": limit,
                "offset": offset,
            }

            return DAOResponse(success=True, data=interactions, meta=meta)
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise CustomException(str(e))
