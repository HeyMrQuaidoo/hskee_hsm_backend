from typing import List, Optional

# models
from app.modules.properties.models.property_assignment import PropertyAssignment

# dao
from app.modules.common.dao.base_dao import BaseDAO


class PropertyAssignmentDAO(BaseDAO[PropertyAssignment]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = PropertyAssignment

        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="property_assignment_id",
        )
