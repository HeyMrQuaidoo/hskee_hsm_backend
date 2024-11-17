from datetime import datetime
from typing import List, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import Depends, Query

# dao
from app.core.response import DAOResponse
from app.modules.billing.dao.transaction_dao import TransactionDAO

# router
from app.modules.billing.enums.billing_enums import PaymentStatusEnum
from app.modules.common.router.base_router import BaseCRUDRouter

# schemas
from app.modules.common.schema.schemas import TransactionSchema
from app.modules.billing.schema.transaction_schema import (
    TransactionCreateSchema,
    TransactionUpdateSchema,
    TransactionResponse,
)

# Core
from app.core.lifespan import get_db


class TransactionRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: TransactionDAO = TransactionDAO(excludes=[])
        TransactionSchema["create_schema"] = TransactionCreateSchema
        TransactionSchema["update_schema"] = TransactionUpdateSchema
        TransactionSchema["response_schema"] = TransactionResponse

        super().__init__(
            dao=self.dao,
            schemas=TransactionSchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/")
        async def get_all_transactions(
            user_id: Optional[UUID] = Query(None),
            transaction_status: Optional[PaymentStatusEnum] = Query(None),
            transaction_number: Optional[str] = Query(None),
            invoice_number: Optional[str] = Query(None),
            transaction_type: Optional[int] = Query(None),
            amount_gte: Optional[float] = Query(None),
            amount_lte: Optional[float] = Query(None),
            date_gte: Optional[datetime] = Query(None),
            date_lte: Optional[datetime] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_transactions(
                db_session=db_session,
                user_id=user_id,
                transaction_status=transaction_status,
                transaction_number=transaction_number,
                invoice_number=invoice_number,
                transaction_type=transaction_type,
                amount_gte=amount_gte,
                amount_lte=amount_lte,
                date_gte=date_gte,
                date_lte=date_lte,
                limit=limit,
                offset=offset,
            )
