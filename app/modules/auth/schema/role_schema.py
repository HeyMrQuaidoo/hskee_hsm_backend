from uuid import UUID
from typing import List, Optional, Annotated
from pydantic import BaseModel, ConfigDict, constr

# models
from app.modules.auth.models.role import Role as RoleModel

# schema
from app.modules.auth.schema.permissions_schema import Permission
from app.modules.auth.schema.mixins.role_mixin import RoleBase


class RoleCreateSchema(RoleBase):
    role_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)


class RoleUpdateSchema(RoleBase):
    role_id: Optional[UUID] = None
    model_config = ConfigDict(from_attributes=True)


class RoleResponse(BaseModel):
    role_id: Optional[UUID] = None
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    permissions: Optional[List[Permission]] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, role: RoleModel):
        """
        Create a RoleResponse instance from an ORM model.

        Args:
            role (RoleModel): Role ORM model.

        Returns:
            RoleResponse: Role response object.
        """
        return cls(
            role_id=role.role_id,
            name=role.name,
            alias=role.alias,
            description=role.description,
            permissions=role.permissions,
        ).model_dump()
