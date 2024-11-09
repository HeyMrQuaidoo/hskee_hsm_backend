from typing import List
from app.modules.common.router.base_router import BaseCRUDRouter
from app.modules.billing.dao.invoice_dao import InvoiceDAO
from app.modules.billing.schema.invoice_schema import (
    InvoiceCreateSchema,
    InvoiceUpdateSchema,
)

from app.modules.common.schema.schemas import InvoiceSchema


class InvoiceRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao = InvoiceDAO()
        InvoiceSchema["create_schema"] = InvoiceCreateSchema
        InvoiceSchema["update_schema"] = InvoiceUpdateSchema

        super().__init__(dao=self.dao, schemas=InvoiceSchema, prefix=prefix, tags=tags)
