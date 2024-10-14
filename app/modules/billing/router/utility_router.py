from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.billing.dao.utility_dao import UtilityDAO
from app.modules.common.router.base_router import BaseCRUDRouter
from app.modules.common.schema.schemas import UtilitySchema
from app.modules.billing.schema.utility_schema import (
    UtilityCreateSchema,
    UtilityUpdateSchema,
    UtilityResponse,
)
from app.core.lifespan import get_db
from app.core.errors import CustomException

class UtilityRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: UtilityDAO = UtilityDAO(excludes=[])
        UtilitySchema["create_schema"] = UtilityCreateSchema
        UtilitySchema["update_schema"] = UtilityUpdateSchema
        UtilitySchema["response_schema"] = UtilityResponse

        super().__init__(dao=self.dao, schemas=UtilitySchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
