from typing import Optional, List

from app.modules.common.dao.base_dao import BaseDAO
from app.modules.resources.models.amenity import Amenities

class AmenityDAO(BaseDAO[Amenities]):
    def __init__(self, excludes: Optional[List[str]] = None):
        super().__init__(model=Amenities, excludes=excludes)
