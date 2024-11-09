from typing import List, Optional

# Models
from app.modules.resources.models.amenities import Amenities

# Base DAO
from app.modules.common.dao.base_dao import BaseDAO


class AmenityDAO(BaseDAO[Amenities]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Amenities
        self.detail_mappings = {}
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="amenity_id",
        )
