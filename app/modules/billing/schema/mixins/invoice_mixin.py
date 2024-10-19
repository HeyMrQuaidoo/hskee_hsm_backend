from uuid import UUID
from datetime import datetime
from typing import Optional, List

# Enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum, InvoiceTypeEnum

# Base schema
from app.modules.common.schema.base_schema import BaseSchema

# Models
from app.modules.billing.models.invoice import Invoice as InvoiceModel
from app.modules.billing.models.invoice_item import InvoiceItem as InvoiceItemModel
from app.modules.auth.models.user import User as UserModel

# Invoice Item Mixins (we'll define this separately)
from app.modules.billing.schema.mixins.invoice_item_mixin import InvoiceItemResponse

class InvoiceBase(BaseSchema):
    issued_by: UUID
    issued_to: UUID
    invoice_details: str
    due_date: datetime
    invoice_type: InvoiceTypeEnum
    status: PaymentStatusEnum

class Invoice(BaseSchema):
    invoice_id: UUID
    invoice_number: str

class InvoiceInfoMixin:
    @classmethod
    def get_invoice_info(cls, invoice: InvoiceModel):
        issued_by_user: UserModel = invoice.issued_by_user
        issued_to_user: UserModel = invoice.issued_to_user

        return {
            "invoice_id": invoice.id,
            "invoice_number": invoice.invoice_number,
            "issued_by": {
                "user_id": issued_by_user.user_id,
                "full_name": issued_by_user.full_name,
            } if issued_by_user else None,
            "issued_to": {
                "user_id": issued_to_user.user_id,
                "full_name": issued_to_user.full_name,
            } if issued_to_user else None,
            "invoice_details": invoice.invoice_details,
            "invoice_amount": invoice.invoice_amount,
            "due_date": invoice.due_date,
            "date_paid": invoice.date_paid,
            "invoice_type": invoice.invoice_type,
            "status": invoice.status,
            "invoice_items": [
                InvoiceItemResponse.model_validate(item) for item in invoice.invoice_items
            ],
        }
