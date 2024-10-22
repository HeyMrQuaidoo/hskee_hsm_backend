from typing import List, Optional

# models
from app.modules.properties.models.unit import Units

# dao
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.resources.dao.media_dao import MediaDAO
from app.modules.address.dao.address_dao import AddressDAO
from app.modules.billing.dao.utility_dao import UtilityDAO
from app.modules.resources.dao.amenity_dao import AmenityDAO


class UnitDAO(BaseDAO[Units]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = Units
        self.detail_mappings = {}
        self.media_dao = MediaDAO()
        self.address_dao = AddressDAO()
        self.utility_dao = UtilityDAO()
        self.amenity_dao = AmenityDAO()

        self.detail_mappings = {
            "media": self.media_dao,
            "amenities": self.amenity_dao,
            "utilities": self.utility_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )
