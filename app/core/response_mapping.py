from pydantic import BaseModel
from typing import Any, Dict, Type
from importlib import import_module

response_mapping: Dict[Type[Any], Type[BaseModel]] = {
    getattr(import_module("app.modules.auth.models.role"), "Role"): getattr(
        import_module("app.modules.auth.schema.role_schema"), "RoleResponse"
    ),
    getattr(
        import_module("app.modules.auth.models.permissions"), "Permissions"
    ): getattr(
        import_module("app.modules.auth.schema.permission"), "PermissionResponse"
    ),
    getattr(import_module("app.modules.auth.models.user"), "User"): getattr(
        import_module("app.modules.auth.schema.user_schema"), "UserSchemaResponse"
    ),
    getattr(
        import_module("app.modules.properties.models.rental_history"),
        "PastRentalHistory",
    ): getattr(
        import_module("app.modules.properties.schema.rental_history_schema"),
        "PastRentalHistoryResponse",
    ),
    getattr(import_module("app.modules.address.models.address"), "Addresses"): getattr(
        import_module("app.modules.address.schema.address_mixin"), "AddressMixin"
    ),
    getattr(import_module("app.modules.billing.models.account"), "Account"): getattr(
        import_module("app.modules.billing.schema.account_schema"), "AccountResponse"
    ),
}
