from typing import List, Optional

# models
from app.modules.properties.models.unit import Units
from app.modules.properties.models.property import Property

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.properties.dao.unit_dao import UnitDAO
from app.modules.resources.dao.media_dao import MediaDAO
from app.modules.address.dao.address_dao import AddressDAO

# schemas


class PropertyDAO(BaseDAO[Property]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = Property

        self.unit_dao = UnitDAO()
        self.media_dao = MediaDAO()
        self.address_dao = AddressDAO()

        self.detail_mappings = {
            "address": self.address_dao,
            "units": self.unit_dao,
            "media": self.media_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )
