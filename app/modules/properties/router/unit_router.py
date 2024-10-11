from typing import List

# dao
from app.modules.properties.dao.unit_dao import UnitDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import PropertySchema
from app.modules.properties.schema.unit_schema import (
    UnitCreateSchema,
    UnitUpdateSchema,
)


class UnitRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        PropertySchema["create_schema"] = UnitCreateSchema
        PropertySchema["update_schema"] = UnitUpdateSchema
        self.dao: UnitDAO = UnitDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=PropertySchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
