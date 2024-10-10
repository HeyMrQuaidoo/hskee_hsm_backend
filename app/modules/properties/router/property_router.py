from typing import List

# dao
from app.modules.properties.dao.property_dao import PropertyDAO

# router
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import PropertySchema
from app.modules.properties.schema.property_schema import (
    PropertyCreateSchema,
    PropertyUpdateSchema,
)


class PropertyRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        PropertySchema["create_schema"] = PropertyCreateSchema
        PropertySchema["update_schema"] = PropertyUpdateSchema
        self.dao: PropertyDAO = PropertyDAO(excludes=[])

        super().__init__(dao=self.dao, schemas=PropertySchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
    #     @self.router.post("/link_property_to_ammenity")
    #     async def add_property_ammenity(
    #         property_unit_assoc_id: UUID,
    #         ammenity_id: UUID,
    #         db: AsyncSession = Depends(self.get_db),
    #     ):
    #         property_ammenity: EntityAmenities = await self.dao.link_entity_to_ammenity(
    #             db_session=db,
    #             property_unit_assoc_id=property_unit_assoc_id,
    #             ammenity_id=ammenity_id,
    #         )

    #         if property_ammenity is None:
    #             raise HTTPException(
    #                 status_code=404, detail="Error adding ammenity to property"
    #             )

    #         return DAOResponse(success=True, data=property_ammenity.to_dict())