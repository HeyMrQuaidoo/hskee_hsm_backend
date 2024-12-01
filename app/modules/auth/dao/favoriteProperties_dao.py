from typing import Optional, List
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.core.response import DAOResponse
from app.modules.common.dao.base_dao import BaseDAO

# Models
from app.modules.auth.models.favorite_properties import FavoriteProperties

# Core
from app.core.errors import CustomException, IntegrityError
from pydantic import UUID4


class FavoritePropertiesDAO(BaseDAO[FavoriteProperties]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = FavoriteProperties

        # Initializing DAOs for related entities if necessary
        self.detail_mappings = {
            # "user": UserDAO(),
            # "property": PropertyDAO(),
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="favorite_id",
        )

    async def get_favorites(
        self,
        db_session: AsyncSession,
        user_id: Optional[UUID4] = None,
        property_unit_assoc_id: Optional[UUID4] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            query = select(self.model)

            # Create a mapping for dynamic filter conditions
            filter_conditions = {
                "user_id": self.model.user_id == user_id if user_id else None,
                "property_unit_assoc_id": self.model.property_unit_assoc_id
                == property_unit_assoc_id
                if property_unit_assoc_id
                else None,
            }

            # Apply filters dynamically
            filters = [
                condition
                for condition in filter_conditions.values()
                if condition is not None
            ]
            if filters:
                query = query.where(*filters)

            # Applying ordering if needed
            query = query.order_by(self.model.favorite_id.desc())

            total_query = select(func.count()).select_from(query.subquery())
            query = query.limit(limit).offset(offset)

            # Executing queries
            result = await db_session.execute(query)
            favorites = result.scalars().all()

            total_items_result = await db_session.execute(total_query)
            total_count = total_items_result.scalar()

            meta = {
                "total_items": total_count,
                "limit": limit,
                "offset": offset,
            }

            return DAOResponse(success=True, data=favorites, meta=meta)
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise CustomException(str(e))
