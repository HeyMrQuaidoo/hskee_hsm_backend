from typing import List, Optional
from datetime import datetime
from fastapi import Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.communication.dao.tour_bookings_dao import TourDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import TourBookingsSchema
from app.modules.communication.schema.tour_bookings_schema import (
    TourCreateSchema,
    TourUpdateSchema,
)

# Enums
from app.modules.communication.enums.communication_enums import TourType, TourStatus

# Core
from app.core.lifespan import get_db
from app.core.response import DAOResponse


class TourRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: TourDAO = TourDAO(excludes=[])
        TourBookingsSchema["create_schema"] = TourCreateSchema
        TourBookingsSchema["update_schema"] = TourUpdateSchema

        super().__init__(
            dao=self.dao,
            schemas=TourBookingsSchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/")
        async def get_all_tours(
            user_id: Optional[UUID4] = Query(None),
            email: Optional[str] = Query(None),
            name: Optional[str] = Query(None),
            phone_number: Optional[str] = Query(None),
            status: Optional[TourStatus] = Query(None),
            tour_type: Optional[TourType] = Query(None),
            date_gte: Optional[datetime] = Query(None),
            date_lte: Optional[datetime] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_tours(
                db_session=db_session,
                user_id=user_id,
                email=email,
                name=name,
                phone_number=phone_number,
                status=status,
                tour_type=tour_type,
                date_gte=date_gte,
                date_lte=date_lte,
                limit=limit,
                offset=offset,
            )
