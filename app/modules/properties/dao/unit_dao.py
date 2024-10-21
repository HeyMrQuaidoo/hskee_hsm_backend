from typing import List, Optional

# models
from app.modules.properties.models.unit import Units

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.address_dao import AddressDAO


class UnitDAO(BaseDAO[Units]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = Units
        self.detail_mappings = {}
        self.address_dao = AddressDAO()

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )
