from pydantic import UUID4
from typing import Optional
from datetime import datetime


from app.modules.common.schema.base_schema import BaseSchema


class UnderContractBase(BaseSchema):
    under_contract_id: UUID4
    property_unit_assoc_id: UUID4
    contract_status: str
    contract_number: str
    client_id: Optional[UUID4] = None
    employee_id: Optional[UUID4] = None
    start_date: datetime
    end_date: datetime
    next_payment_due: datetime
