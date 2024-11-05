from uuid import UUID
from typing import List, Optional, Annotated, Union
from pydantic import BaseModel, ConfigDict, constr

# schema
from app.modules.common.schema.base_schema import BaseSchema

# models
from app.modules.auth.models.permissions import Permissions as PermissionsModel


class Role(BaseSchema):
    role_id: Optional[UUID] = None
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None


class PermissionBase(BaseSchema):
    description: Optional[str] = None
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    # roles: Optional[Union[List[Role]]] = None #comment


class Permission(PermissionBase):
    permission_id: Optional[UUID] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "permission_id": "123e4567-e89b-12d3-a456-426614174000",
                "name": "Administrator",
                "alias": "admin",
                "description": "Has full access to all settings.",
            }
        },
    )


class PermissionCreateSchema(PermissionBase):
    model_config = ConfigDict(from_attributes=True)


class PermissionUpdateSchema(PermissionBase):
    model_config = ConfigDict(from_attributes=True)


class PermissionsResponse(BaseSchema):
    permission_id: Optional[UUID] = None
    name: Optional[Annotated[str, constr(max_length=80)]] = None
    alias: Optional[Annotated[str, constr(max_length=80)]] = None
    description: Optional[str] = None
    roles: Optional[List[Role]] = None

    @classmethod
    def model_validate(cls, permission: PermissionsModel):
        """
        Create a PermissionResponse instance from an ORM model.

        Args:
            permission (PermissionsModel): Permission ORM model.

        Returns:
            PermissionResponse: Permission response object.
        """
        return cls(
            permission=permission.permission_id,
            name=permission.name,
            alias=permission.alias,
            description=permission.description,
            roles=permission.roles,
        ).model_dump()
