from typing import List

# dao
from app.modules.properties.dao.property_dao import PropertyDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import PropertySchema
from app.modules.properties.schema.property_schema import (
    PropertyCreateSchema,
    PropertyUpdateSchema,
)


class PropertyRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        self.dao: PropertyDAO = PropertyDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=PropertySchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
