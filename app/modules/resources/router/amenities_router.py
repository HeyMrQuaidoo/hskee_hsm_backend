from typing import List
from app.modules.common.router.base_router import BaseCRUDRouter
from app.modules.resources.dao.amenity_dao import AmenityDAO
from app.modules.resources.schema.amenities_schema import AmenityCreateSchema, AmenityUpdateSchema

from app.modules.common.schema.schemas import AmenitiesSchema

class AmenityRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao = AmenityDAO()
        AmenitiesSchema["create_schema"] = AmenityCreateSchema
        AmenitiesSchema["update_schema"] = AmenityUpdateSchema

        super().__init__(dao=self.dao, schemas=AmenitiesSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass