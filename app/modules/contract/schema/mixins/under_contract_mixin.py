from uuid import UUID
from datetime import datetime
from typing import List, Optional

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# schemas
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.auth.schema.mixins.user_mixin import UserBase
from app.modules.contract.schema.mixins.contract_mixin import ContractBase
from app.modules.properties.schema.mixins.property_mixin import PropertyBase


class UnderContractBase(BaseSchema):
    property_unit_assoc_id: UUID
    contract_status: Optional[ContractStatusEnum]
    contract_number: str
    client_id: Optional[UUID] = None
    employee_id: Optional[UUID] = None
    start_date: datetime
    end_date: datetime
    next_payment_due: datetime
    properties: Optional[List[PropertyBase]] = []
    contract: Optional[List[ContractBase]] = []
    employee_representative: Optional[List[UserBase]] = []
    client_representative: Optional[List[UserBase]] = []


class UnderContract(BaseSchema):
    under_contract_id: Optional[UUID]
