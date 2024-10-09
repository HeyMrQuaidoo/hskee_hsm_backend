from typing import List, Optional

# models
from app.modules.auth.models.user import User

# dao
from app.modules.auth.dao.role_dao import RoleDAO
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.billing.dao.account_dao import AccountDAO
from app.modules.address.dao.address_dao import AddressDAO
from app.modules.properties.models.rental_history import PastRentalHistory


class UserDAO(BaseDAO[User]):
    def __init__(self, excludes: Optional[List[str]]):
        self.model = User

        self.role_dao = RoleDAO()
        self.address_dao = AddressDAO()
        self.account_dao = AccountDAO()
        self.rental_history_dao = BaseDAO(
            model=PastRentalHistory,
            detail_mappings={"address": self.address_dao},
            excludes=excludes,
            primary_key="rental_history_id",
        )
        self.detail_mappings = {
            "address": self.address_dao,
            "roles": self.role_dao,
            "rental_history": self.rental_history_dao,
            "accounts": self.account_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="user_id",
        )
