from datetime import datetime
from typing import Optional, List
from pydantic import ConfigDict
from uuid import UUID

# Enums
from app.modules.billing.enums.billing_enums import PaymentStatusEnum, InvoiceTypeEnum

# Base Faker
from app.modules.common.schema.base_schema import BaseFaker

# Mixins
from app.modules.billing.schema.mixins.invoice_mixin import (
    InvoiceBase,
    InvoiceInfoMixin,
    Invoice,
)
from app.modules.billing.schema.mixins.invoice_item_mixin import InvoiceItemBase, InvoiceItemResponse 

# Models
from app.modules.billing.models.invoice import Invoice as InvoiceModel

class InvoiceCreateSchema(InvoiceBase):
    invoice_items: Optional[List[InvoiceItemBase]] = []

    # Faker attributes
    _issued_by = str(BaseFaker.uuid4())
    _issued_to = str(BaseFaker.uuid4())
    _invoice_details = BaseFaker.text(max_nb_chars=200)
    _due_date = BaseFaker.future_datetime()
    _invoice_type = BaseFaker.random_element([e.value for e in InvoiceTypeEnum])
    _status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "issued_by": _issued_by,
                "issued_to": _issued_to,
                "invoice_details": _invoice_details,
                "due_date": _due_date.isoformat(),
                "invoice_type": _invoice_type,
                "status": _status,
                "invoice_items": [
                    {
                        "description": BaseFaker.sentence(),
                        "quantity": BaseFaker.random_int(min=1, max=10),
                        "unit_price": round(BaseFaker.random_number(digits=5), 2),
                        "reference_id": str(BaseFaker.uuid4()),
                    },
                ],
            }
        },
    )

class InvoiceUpdateSchema(InvoiceBase):
    issued_by: Optional[UUID] = None
    issued_to: Optional[UUID] = None
    invoice_details: Optional[str] = None
    due_date: Optional[datetime] = None
    date_paid: Optional[datetime] = None
    invoice_type: Optional[InvoiceTypeEnum] = None
    status: Optional[PaymentStatusEnum] = None

    # Faker attributes
    _issued_by = str(BaseFaker.uuid4())
    _issued_to = str(BaseFaker.uuid4())
    _invoice_details = BaseFaker.text(max_nb_chars=200)
    _due_date = BaseFaker.future_datetime()
    _date_paid = BaseFaker.date_time_this_year()
    _invoice_type = BaseFaker.random_element([e.value for e in InvoiceTypeEnum])
    _status = BaseFaker.random_element([e.value for e in PaymentStatusEnum])

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "issued_by": _issued_by,
                "issued_to": _issued_to,
                "invoice_details": _invoice_details,
                "due_date": _due_date.isoformat(),
                "date_paid": _date_paid.isoformat(),
                "invoice_type": _invoice_type,
                "status": _status,
            }
        },
    )

class InvoiceResponse(InvoiceBase, InvoiceInfoMixin):
    invoice_id: UUID
    invoice_number: str
    invoice_amount: float
    date_paid: Optional[datetime] = None
    invoice_items: Optional[List[InvoiceItemResponse]] = []

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "invoice_id": str(BaseFaker.uuid4()),
                "invoice_number": f"INV{BaseFaker.random_number(digits=8)}",
                "issued_by": str(BaseFaker.uuid4()),
                "issued_to": str(BaseFaker.uuid4()),
                "invoice_details": BaseFaker.text(max_nb_chars=200),
                "due_date": BaseFaker.future_datetime().isoformat(),
                "date_paid": BaseFaker.date_time_this_year().isoformat(),
                "invoice_type": BaseFaker.random_element([e.value for e in InvoiceTypeEnum]),
                "status": BaseFaker.random_element([e.value for e in PaymentStatusEnum]),
                "invoice_amount": round(BaseFaker.random_number(digits=5), 2),
                "invoice_items": [
                    {
                        "invoice_item_id": str(BaseFaker.uuid4()),
                        "description": BaseFaker.sentence(),
                        "quantity": BaseFaker.random_int(min=1, max=10),
                        "unit_price": round(BaseFaker.random_number(digits=5), 2),
                        "total_price": round(BaseFaker.random_number(digits=6), 2),
                        "reference_id": str(BaseFaker.uuid4()),
                    },
                ],
            }
        },
    )

    @classmethod
    def model_validate(cls, invoice: InvoiceModel):
        invoice_info = cls.get_invoice_info(invoice)
        return cls(**invoice_info)
