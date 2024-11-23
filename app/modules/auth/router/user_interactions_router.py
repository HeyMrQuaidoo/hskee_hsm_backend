# user_interactions_router.py

from typing import List, Optional
from datetime import datetime
from fastapi import Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.auth.dao.user_interactions_dao import UserInteractionsDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import UserInteractionsSchema
from app.modules.auth.schema.user_interactions_schema import (
    UserInteractionsCreateSchema,
    UserInteractionsUpdateSchema,
)

# Core
from app.core.lifespan import get_db
from app.core.response import DAOResponse


class UserInteractionsRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: UserInteractionsDAO = UserInteractionsDAO(excludes=[])
        UserInteractionsSchema["create_schema"] = UserInteractionsCreateSchema
        UserInteractionsSchema["update_schema"] = UserInteractionsUpdateSchema

        super().__init__(
            dao=self.dao,
            schemas=UserInteractionsSchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/")
        async def get_all_interactions(
            user_id: Optional[UUID4] = Query(None),
            employee_id: Optional[UUID4] = Query(None),
            property_unit_assoc_id: Optional[UUID4] = Query(None),
            date_gte: Optional[datetime] = Query(None),
            date_lte: Optional[datetime] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_interactions(
                db_session=db_session,
                user_id=user_id,
                employee_id=employee_id,
                property_unit_assoc_id=property_unit_assoc_id,
                date_gte=date_gte,
                date_lte=date_lte,
                limit=limit,
                offset=offset,
            )
