from uuid import UUID
from typing import Optional

# Base schema
from app.modules.common.schema.base_schema import BaseSchema

# Models
from app.modules.billing.models.invoice_item import InvoiceItem as InvoiceItemModel

class InvoiceItemBase(BaseSchema):
    description: Optional[str] = None
    quantity: int
    unit_price: float
    reference_id: Optional[str] = None

class InvoiceItem(BaseSchema):
    invoice_item_id: UUID
    total_price: float

class InvoiceItemResponse(InvoiceItemBase):
    invoice_item_id: UUID
    total_price: float

    @classmethod
    def model_validate(cls, invoice_item: InvoiceItemModel):
        return cls(
            invoice_item_id=invoice_item.invoice_item_id,
            description=invoice_item.description,
            quantity=invoice_item.quantity,
            unit_price=invoice_item.unit_price,
            total_price=invoice_item.total_price,
            reference_id=invoice_item.reference_id,
        )
