# models
from app.modules.auth.models.user import User
from app.modules.auth.models.role import Role
from app.modules.auth.models.permissions import Permissions
from app.modules.billing.models.account import Account
from app.modules.properties.models.property import Property

# schema
from app.modules.common.schema.base_schema import CustomBaseModel


RoleSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Role, excludes=["role_id"]
)

AccountSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Account, excludes=["account_id"]
)

PropertySchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Property, excludes=["property_unit_assoc_id"]
)

PermissionSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Permissions, excludes=["permission_id"]
)

UserSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    User, excludes=["user_id"]
)
