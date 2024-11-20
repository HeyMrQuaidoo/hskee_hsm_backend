from uuid import UUID
from typing import List, Optional, Union

# schema
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.auth.schema.permissions_schema import Permission


class RoleBase(BaseSchema):
    role_id: Optional[UUID] = None
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Union[List[Permission]]] = []


class Role(RoleBase):
    role_id: Optional[UUID] = None
