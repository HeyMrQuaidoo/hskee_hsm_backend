from typing import List
from uuid import UUID
from fastapi import Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.billing.dao.transaction_dao import TransactionDAO

# Base CRUD Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import TransactionSchema
from app.modules.billing.schema.transaction_schema import (
    TransactionCreateSchema,
    TransactionUpdateSchema,
    TransactionResponse,
)

# Core
from app.core.lifespan import get_db
from app.core.errors import CustomException

class TransactionRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: TransactionDAO = TransactionDAO(excludes=[])
        TransactionSchema["create_schema"] = TransactionCreateSchema
        TransactionSchema["update_schema"] = TransactionUpdateSchema
        TransactionSchema["response_schema"] = TransactionResponse

        super().__init__(dao=self.dao, schemas=TransactionSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        pass
