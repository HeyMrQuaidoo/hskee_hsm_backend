from typing import List, Optional

# models
from app.modules.properties.models.rental_history import PastRentalHistory

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.address_dao import AddressDAO


class PastRentalHistoryDAO(BaseDAO[PastRentalHistory]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = PastRentalHistory
        self.address_dao = AddressDAO()

        self.detail_mappings = {
            "address": self.address_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="rental_history_id",
        )
