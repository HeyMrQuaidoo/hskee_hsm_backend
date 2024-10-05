from typing import List, Optional

# models
from app.modules.properties.models.unit import Units
from app.modules.properties.models.property import Property

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.address_dao import AddressDAO

# schemas


class PropertyDAO(BaseDAO[Property]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Property

        self.address_dao = AddressDAO()
        self.unit_dao = BaseDAO(
            model=Units,
            detail_mappings={"address": self.address_dao},
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )
        self.detail_mappings = {"address": self.address_dao, "units": self.unit_dao}
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )
