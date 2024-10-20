from typing import Optional, List

# Base DAO and related imports
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.billing.models.invoice import Invoice
# from app.modules.billing.dao.transaction_dao import TransactionDAO
from app.modules.auth.dao.user_dao import UserDAO
# from app.modules.billing.dao.invoice_item_dao import InvoiceItemDAO

class InvoiceDAO(BaseDAO[Invoice]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Invoice

        # DAOs for related entities
        # self.transaction_dao = TransactionDAO()
        # self.user_dao = UserDAO()
        # self.invoice_item_dao = InvoiceItemDAO()

        # Detail mappings to resolve relationships
        self.detail_mappings = {
            # "transaction": self.transaction_dao,
            # "issued_by_user": self.user_dao,
            # "issued_to_user": self.user_dao,
            # "invoice_items": self.invoice_item_dao,
        }

        # Call the base DAO with appropriate arguments
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="id",
        )
