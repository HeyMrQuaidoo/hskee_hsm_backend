from typing import List

# dao
from app.modules.billing.dao.utility_dao import UtilityDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import UtilitiesSchema
from app.modules.billing.schema.utility_schema import (
    UtilityCreateSchema,
    UtilityUpdateSchema,
)


class UtilityRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        UtilitiesSchema["create_schema"] = UtilityCreateSchema
        UtilitiesSchema["update_schema"] = UtilityUpdateSchema
        self.dao: UtilityDAO = UtilityDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=UtilitiesSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
