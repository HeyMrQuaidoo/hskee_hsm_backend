from typing import List

# dao
from app.modules.properties.dao.property_assignment_dao import PropertyAssignmentDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import PropertyAssignmentSchema
from app.modules.properties.schema.property_assignment_schema import (
    PropertyAssignmentCreate,
    PropertyAssignmentUpdate,
)


class PropertyAssignmentRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        PropertyAssignmentSchema["create_schema"] = PropertyAssignmentCreate
        PropertyAssignmentSchema["update_schema"] = PropertyAssignmentUpdate
        self.dao: PropertyAssignmentDAO = PropertyAssignmentDAO(excludes=[])

        super().__init__(
            dao=self.dao, schemas=PropertyAssignmentSchema, prefix=prefix, tags=tags
        )
        self.register_routes()

    def register_routes(self):
        pass
