from datetime import datetime
from typing import List, Optional
from uuid import UUID
from fastapi import Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession


from app.core.response import DAOResponse
from app.modules.common.router.base_router import BaseCRUDRouter
from app.modules.billing.dao.invoice_dao import InvoiceDAO
from app.modules.billing.schema.invoice_schema import (
    InvoiceCreateSchema,
    InvoiceUpdateSchema,
)

from app.modules.common.schema.schemas import InvoiceSchema

# Core
from app.core.lifespan import get_db


class InvoiceRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao = InvoiceDAO()
        InvoiceSchema["create_schema"] = InvoiceCreateSchema
        InvoiceSchema["update_schema"] = InvoiceUpdateSchema

        super().__init__(
            dao=self.dao,
            schemas=InvoiceSchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/statistics/trends")
        async def get_invoice_trends(
            month: Optional[int] = Query(None, ge=1, le=12),
            year: Optional[int] = Query(None, ge=1900),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_invoice_trends(
                db_session=db_session,
                month=month,
                year=year,
            )

        @self.router.get("/")
        async def filter_invoices(
            invoice_number: Optional[str] = Query(None),
            issued_by: Optional[UUID] = Query(None),
            issued_to: Optional[UUID] = Query(None),
            invoice_type: Optional[str] = Query(None),
            status: Optional[str] = Query(None),
            min_amount: Optional[float] = Query(None),
            max_amount: Optional[float] = Query(None),
            due_date_from: Optional[datetime] = Query(None),
            due_date_to: Optional[datetime] = Query(None),
            db_session: AsyncSession = Depends(get_db),
        ):
            return await self.dao.filter_invoices(
                db_session=db_session,
                invoice_number=invoice_number,
                issued_by=issued_by,
                issued_to=issued_to,
                invoice_type=invoice_type,
                status=status,
                min_amount=min_amount,
                max_amount=max_amount,
                due_date_from=due_date_from,
                due_date_to=due_date_to,
            )
