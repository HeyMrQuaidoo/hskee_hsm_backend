from typing import List, Optional
from fastapi import Depends, Query
from pydantic import UUID4
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.auth.dao.favoriteProperties_dao import FavoritePropertiesDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import FavoritePropertiesSchema
from app.modules.auth.schema.favorite_properties_schema import (
    FavoritePropertiesUpdateSchema,
    FavoritePropertiesCreateSchema,
)

# Core
from app.core.lifespan import get_db
from app.core.response import DAOResponse


class FavoritePropertiesRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: FavoritePropertiesDAO = FavoritePropertiesDAO(excludes=[])
        FavoritePropertiesSchema["create_schema"] = FavoritePropertiesCreateSchema
        FavoritePropertiesSchema["update_schema"] = FavoritePropertiesUpdateSchema

        super().__init__(
            dao=self.dao,
            schemas=FavoritePropertiesSchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/")
        async def get_all_favorites(
            user_id: Optional[UUID4] = Query(None),
            property_unit_assoc_id: Optional[UUID4] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_favorites(
                db_session=db_session,
                user_id=user_id,
                property_unit_assoc_id=property_unit_assoc_id,
                limit=limit,
                offset=offset,
            )
