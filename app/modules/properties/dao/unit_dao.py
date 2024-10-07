from typing import List, Optional

# models
from app.modules.properties.models.unit import Units

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.address_dao import AddressDAO

# schemas


class UnitDAO(BaseDAO[Units]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Units

        self.address_dao = AddressDAO()
        self.detail_mappings = {}
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )
