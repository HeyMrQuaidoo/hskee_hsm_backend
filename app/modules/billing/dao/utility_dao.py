from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession


from app.modules.common.dao.base_dao import BaseDAO

# enums
from app.modules.billing.enums.billing_enums import BillableTypeEnum

# shemas
from app.modules.billing.schema.utility_schema import UtilityCreateSchema

# models
from app.modules.billing.models.utility import Utilities
from app.modules.associations.models.entity_billable import EntityBillable


class UtilityDAO(BaseDAO[Utilities]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Utilities
        self.detail_mappings = {}
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="utility_id",
        )

    async def create(
        self,
        db_session: AsyncSession,
        obj_in: UtilityCreateSchema,
    ) -> Utilities:
        # Create Utility
        utility_data = {
            "name": obj_in.name,
            "description": obj_in.description,
        }
        utility = Utilities(**utility_data)
        db_session.add(utility)
        await db_session.flush()

        # Create EntityBillable association
        entity_billable = EntityBillable(
            entity_id=str(obj_in.entity_id),
            entity_type=obj_in.entity_type,
            billable_id=utility.billable_assoc_id,
            billable_type=BillableTypeEnum.utilities,
            billable_amount=obj_in.billable_amount,
        )
        db_session.add(entity_billable)
        await db_session.commit()
        return utility
