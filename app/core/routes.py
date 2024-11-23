from fastapi import APIRouter, FastAPI

# TODO (DQ) Add custom routes
# Issue: https://github.com/compylertech/hskee-hsm-backend/issues/3

from app.modules.auth.router.auth_router import AuthRouter
from app.modules.auth.router.permission_router import PermissionRouter
from app.modules.auth.router.role_router import RoleRouter
from app.modules.auth.router.favorite_properties_router import FavoritePropertiesRouter
from app.modules.auth.router.user_interactions_router import UserInteractionsRouter
from app.modules.auth.router.user_router import UserRouter
from app.modules.billing.router.account_router import AccountRouter
from app.modules.billing.router.invoice_router import InvoiceRouter
from app.modules.billing.router.payment_type_router import PaymentTypeRouter
from app.modules.billing.router.transaction_router import TransactionRouter
from app.modules.billing.router.transaction_type_router import TransactionTypeRouter
from app.modules.billing.router.utility_router import UtilityRouter
from app.modules.common.router.calendar_event_router import CalendarEventRouter
from app.modules.communication.router.maintenance_request_router import (
    MaintenanceRequestRouter,
)
from app.modules.communication.router.message_router import MessageRouter
from app.modules.communication.router.tour_bookings_router import TourRouter
from app.modules.contract.router.contract_router import ContractRouter
from app.modules.contract.router.contract_type_router import ContractTypeRouter
from app.modules.contract.router.under_contract_router import UnderContractRouter
from app.modules.properties.router.property_assignment_router import (
    PropertyAssignmentRouter,
)
from app.modules.properties.router.property_router import PropertyRouter
from app.modules.properties.router.unit_router import UnitRouter
from app.modules.resources.router.amenities_router import AmenityRouter
from app.modules.resources.router.media_router import MediaRouter

router = APIRouter()


def configure_routes(app: FastAPI):
    app.include_router(router)

    # Router configuration list
    router_configurations = [
        (AccountRouter, "/account", ["Account"]),
        (AmenityRouter, "/amenities", ["Amenities"]),
        (AuthRouter, "/auth", ["Auth"]),
        (CalendarEventRouter, "/calendar-event", ["Calendar Event"]),
        (ContractRouter, "/contract", ["Contract"]),
        (ContractTypeRouter, "/contract-type", ["Contract Type"]),
        (FavoritePropertiesRouter, "/favorite-properties", ["Favorite Properties"]),
        (InvoiceRouter, "/invoice", ["Invoices"]),
        (MaintenanceRequestRouter, "/maintenance-request", ["Maintenance Request"]),
        (MediaRouter, "/media", ["Media"]),
        (MessageRouter, "/message", ["Message"]),
        (PaymentTypeRouter, "/payment-type", ["Payment Type"]),
        (PermissionRouter, "/permissions", ["Permissions"]),
        (PropertyRouter, "/property", ["Property"]),
        (PropertyAssignmentRouter, "/assign-properties", ["PropertyAssignments"]),
        (RoleRouter, "/roles", ["Roles"]),
        (TourRouter, "/tour", ["Tour Bookings"]),
        (TransactionRouter, "/transaction", ["Transaction"]),
        (TransactionTypeRouter, "/transaction-type", ["Transaction Type"]),
        (UnderContractRouter, "/assign-contracts", ["Under Contracts"]),
        (UnitRouter, "/unit", ["Unit"]),
        (UserInteractionsRouter, "/user-interactions", ["User Interactions"]),
        (UserRouter, "/users", ["Users"]),
        (UtilityRouter, "/utilities", ["Utilities"]),
    ]

    # Automatically include routers
    for router_cls, prefix, tags in router_configurations:
        app.include_router(router_cls(prefix=prefix, tags=tags).router)

    return app
