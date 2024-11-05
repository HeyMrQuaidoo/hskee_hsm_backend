from fastapi import APIRouter, FastAPI

# TODO (DQ) Add custom routes
# Issue: https://github.com/compylertech/hskee-hsm-backend/issues/3

from app.modules.auth.router.role_router import RoleRouter
from app.modules.auth.router.user_router import UserRouter
from app.modules.billing.router.invoice_router import InvoiceRouter
from app.modules.billing.router.payment_type_router import PaymentTypeRouter
from app.modules.billing.router.transaction_router import TransactionRouter
from app.modules.billing.router.transaction_type_router import TransactionTypeRouter
from app.modules.billing.router.utility_router import UtilityRouter
from app.modules.common.router.calendar_event_router import CalendarEventRouter
from app.modules.communication.router.maintenance_request_router import (
    MaintenanceRequestRouter,
)
from app.modules.contract.router.contract_router import ContractRouter
from app.modules.contract.router.contract_type_router import ContractTypeRouter
from app.modules.contract.router.under_contract_router import UnderContractRouter
from app.modules.properties.router.property_assignment_router import PropertyAssignmentRouter
from app.modules.properties.router.unit_router import UnitRouter
from app.modules.resources.router.amenities_router import AmenityRouter
from app.modules.resources.router.media_router import MediaRouter
from app.modules.billing.router.account_router import AccountRouter
from app.modules.auth.router.permission_router import PermissionRouter
from app.modules.properties.router.property_router import PropertyRouter
from app.modules.auth.router.auth_router import AuthRouter

router = APIRouter()


def configure_routes(app: FastAPI):
    app.include_router(router)

    # Create an instance of AuthRouter
    app.include_router(AuthRouter(prefix="/auth", tags=["Auth"]).router)

    # Create an instance of RoleRouter
    app.include_router(RoleRouter(prefix="/roles", tags=["Roles"]).router)

    # app.include_router(
    #     BaseCRUDRouter(
    #         dao=BaseDAO(
    #             model=Role,
    #             excludes=["users"],
    #             detail_mappings={
    #                 "permissions": BaseDAO(
    #                     model=Permissions,
    #                     detail_mappings={},
    #                     excludes=[],
    #                     primary_key="permission_id",
    #                 ),
    #                 "address": AddressDAO(),
    #             },
    #             primary_key="role_id",
    #         ),
    #         schemas={
    #             **RoleSchema,
    #             "create_schema": RoleCreateSchema,
    #             "update_schema": RoleUpdateSchema,
    #         },
    #         prefix="/sample",
    #         tags=["Sample"],
    #     ).router
    # )

    # Create an instance of PermissionRouter
    app.include_router(
        PermissionRouter(prefix="/permissions", tags=["Permissions"]).router
    )

    # Create an instance of UserRouter
    app.include_router(UserRouter(prefix="/users", tags=["Users"]).router)

    # Create an instance of PropertyRouter
    app.include_router(PropertyRouter(prefix="/property", tags=["Property"]).router)

    # Create an instance of ContractRouter
    app.include_router(ContractRouter(prefix="/contract", tags=["Contract"]).router)

    # Create an instance of PaymentTypeRouter
    app.include_router(
        PaymentTypeRouter(prefix="/payment-type", tags=["Payment Type"]).router
    )

    # Create an instance of TransactionRouter
    app.include_router(
        TransactionRouter(prefix="/transaction", tags=["Transaction"]).router
    )
    # Create an instance of TransactionTypeRouter
    app.include_router(
        TransactionTypeRouter(
            prefix="/transaction-type", tags=["Transaction Type"]
        ).router
    )

    # Create an instance of ContractTypeRouter
    app.include_router(
        ContractTypeRouter(prefix="/contract-type", tags=["Contract Type"]).router
    )

    # Create an instance of UnitRouter
    app.include_router(UnitRouter(prefix="/unit", tags=["Unit"]).router)

    # Create an instance of MediaRouter
    app.include_router(MediaRouter(prefix="/media", tags=["Media"]).router)

    app.include_router(AmenityRouter(prefix="/amenities", tags=["Amenities"]).router)

    app.include_router(UtilityRouter(prefix="/utilities", tags=["Utilities"]).router)

    app.include_router(InvoiceRouter(prefix="/invoice", tags=["Invoices"]).router)

    app.include_router(
        UnderContractRouter(prefix="/assign-contracts", tags=["Under Contracts"]).router
    )
    app.include_router(
        PropertyAssignmentRouter(
            prefix="/assign-properties", tags=["PropertyAssignments"]
        ).router
    )

    # Create an instance of AccountRouter
    app.include_router(AccountRouter(prefix="/account", tags=["Account"]).router)

    # Create an instance of MaintenanceRequestRouter
    app.include_router(
        MaintenanceRequestRouter(
            prefix="/maintenance-request", tags=["Maintenance Request"]
        ).router
    )

    # Create an instance of EventTypeRouter
    app.include_router(
        CalendarEventRouter(prefix="/calendar-event", tags=["Calendar Event"]).router
    )

    return app