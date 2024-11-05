# app/modules/contract/router/under_contract_router.py

from typing import List
from app.modules.common.router.base_router import BaseCRUDRouter
from app.modules.contract.dao.under_contract_dao import UnderContractDAO
from app.modules.contract.schema.under_contract_schema import (
    UnderContractCreateSchema,
    UnderContractUpdateSchema,
)
from app.modules.common.schema.schemas import UnderContractSchema


class UnderContractRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        # Initialize the DAO for UnderContract
        self.dao = UnderContractDAO()

        # Define the schemas for create and update operations
        UnderContractSchema["create_schema"] = UnderContractCreateSchema
        UnderContractSchema["update_schema"] = UnderContractUpdateSchema

        super().__init__(
            dao=self.dao, schemas=UnderContractSchema, prefix=prefix, tags=tags
        )
