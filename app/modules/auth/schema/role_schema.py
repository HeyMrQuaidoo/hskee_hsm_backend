from uuid import UUID
from pydantic import UUID4
from pydantic import BaseModel, ConfigDict, constr
from typing import List, Optional, Annotated, Union

# models
from app.modules.auth.models.role import Role as RoleModel

# schema
from app.modules.auth.schema.permission import Permission
from app.modules.common.schema.base_schema import BaseSchema


class RoleBase(BaseSchema):
    name: str
    alias: Optional[str] = None
    description: Optional[str] = None
    permissions: Optional[Union[List[Permission]]] = []


class Role(RoleBase):
    role_id: UUID4


class RoleCreateSchema(RoleBase):
    model_config = ConfigDict(from_attributes=True)


class RoleUpdateSchema(RoleBase):
    model_config = ConfigDict(from_attributes=True)


class RoleResponse(BaseModel):
    role_id: UUID
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    permissions: Optional[List[Permission]] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_orm(cls, role: RoleModel):
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
