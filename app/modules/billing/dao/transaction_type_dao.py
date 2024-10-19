from typing import List, Optional

# Models
from app.modules.billing.models.transaction_type import TransactionType

# DAO
from app.modules.common.dao.base_dao import BaseDAO


class TransactionTypeDAO(BaseDAO[TransactionType]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = TransactionType

        # Define relationships or additional DAOs if necessary
        self.detail_mappings = {}  # Add related DAOs here if needed

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="transaction_type_id",  # Assuming `transaction_type_id` is the primary key
        )
