from typing import Optional, List

from app.modules.common.dao.base_dao import BaseDAO
from app.modules.billing.models.utility import Utilities


class UtilityDAO(BaseDAO[Utilities]):
    def __init__(self, excludes: Optional[List[str]] = None):
        super().__init__(model=Utilities, excludes=excludes)
