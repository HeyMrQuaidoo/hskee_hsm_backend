from typing import List, Union

# schemas
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.address.schema.address_mixin import AddressMixin

# models
from app.modules.billing.models.account import Account as AccountModel


class AccountMixin(BaseSchema, AddressMixin):
    @classmethod
    def get_account_info(
        cls, accounts: Union[AccountModel | List[AccountModel]]
    ) -> List[AccountModel]:
        # create account model for each entity_account
        if not accounts and len(accounts) == 0:
            return []

        if isinstance(accounts, list):
            result = []

            for account in accounts:
                account_obj = cls(
                    account_id=account.account_id,
                    account_branch_name=account.account_branch_name,
                    address=cls.get_address_base(account.address),
                    bank_account_name=account.bank_account_name,
                    bank_account_number=account.bank_account_number,
                ).model_dump()

                for entity_account in account.entity_accounts:
                    account_obj = {
                        **account_obj,
                        "account_type": entity_account.account_type,
                    }

                result.append(account_obj)
        else:
            result = cls(
                account_id=accounts.account_id,
                account_branch_name=accounts.account_branch_name,
                address=cls.get_address_base(accounts.address),
                bank_account_name=accounts.bank_account_name,
                bank_account_number=accounts.bank_account_number,
            ).model_dump()

            for entity_account in accounts.entity_accounts:
                result = {
                    **result,
                    "account_type": entity_account.account_type,
                }
        return result
