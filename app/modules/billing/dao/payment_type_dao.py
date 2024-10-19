from typing import List, Optional

# Models
from app.modules.billing.models.payment_type import PaymentType

# DAO
from app.modules.common.dao.base_dao import BaseDAO


class PaymentTypeDAO(BaseDAO[PaymentType]):
    def __init__(self, excludes: Optional[List[str]] = [""]):
        self.model = PaymentType

        # Define relationships or additional DAOs if necessary
        self.detail_mappings = {}  # Add related DAOs here if needed
        
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="payment_type_id",  # Assuming `payment_type_id` is the primary key
        )
