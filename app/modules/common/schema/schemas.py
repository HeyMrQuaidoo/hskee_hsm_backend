# models
from app.modules.auth.models.user import User
from app.modules.auth.models.role import Role
from app.modules.billing.models.payment_type import PaymentType
from app.modules.billing.models.transaction import Transaction
from app.modules.billing.models.transaction_type import TransactionType
from app.modules.contract.models.contract_type import ContractType
from app.modules.resources.models.media import Media
from app.modules.properties.models.unit import Units
from app.modules.billing.models.account import Account
from app.modules.contract.models.contract import Contract
from app.modules.billing.models.utility import Utilities
from app.modules.auth.models.permissions import Permissions
from app.modules.properties.models.property import Property
from app.modules.properties.models.property_assignment import PropertyAssignment

# schema
from app.modules.common.schema.base_schema import CustomBaseModel


RoleSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Role, excludes=["role_id"]
)

AccountSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Account, excludes=["account_id"]
)

ContractSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Contract, excludes=["contract_number"]
)

TransactionTypeSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    TransactionType, excludes=["transaction_type_id"]
)

TransactionSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Transaction, excludes=["transaction_id"]
)

PaymentTypeSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    PaymentType, excludes=["payment_type_id"]
)

ContractTypeSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    ContractType, excludes=["contract_type_id"]
)


UtilitySchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Utilities, excludes=["billable_assoc_id"]
)

PropertySchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Property, excludes=["property_unit_assoc_id"]
)

UnitSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Units, excludes=["property_unit_assoc_id"]
)

PropertyAssignmentSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    PropertyAssignment, excludes=["property_assignment_id"]
)

MediaSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Media, excludes=["media_id"]
)

PermissionSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    Permissions, excludes=["permission_id"]
)

UserSchema = CustomBaseModel.generate_schemas_for_sqlalchemy_model(
    User, excludes=["user_id"]
)
