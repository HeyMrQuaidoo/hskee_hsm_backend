from typing import Optional, List


from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.billing.models.utility import Utilities


class UtilityDAO(BaseDAO[Utilities]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Utilities
        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="utility_id",
        )