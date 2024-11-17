from datetime import datetime
from typing import Optional, List
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.orm import aliased
from sqlalchemy.ext.asyncio import AsyncSession


# dao
from app.core.response import DAOResponse
from app.modules.billing.enums.billing_enums import PaymentStatusEnum
from app.modules.billing.models.invoice import Invoice
from app.modules.common.dao.base_dao import BaseDAO

# models
from app.modules.billing.models.transaction import Transaction
from app.modules.billing.dao.invoice_dao import InvoiceDAO
from app.modules.billing.dao.payment_type_dao import PaymentTypeDAO
from app.modules.billing.dao.transaction_type_dao import TransactionTypeDAO
from app.modules.auth.dao.user_dao import UserDAO

# core
from app.core.errors import CustomException, IntegrityError, RecordNotFoundException


class TransactionDAO(BaseDAO[Transaction]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Transaction
        self.invoice_model = Invoice

        # DAOs for related entities
        self.invoice_dao = InvoiceDAO()
        self.payment_type_dao = PaymentTypeDAO()
        self.transaction_type_dao = TransactionTypeDAO()
        self.user_dao = UserDAO()

        # Detail mappings for creating related entities
        self.detail_mappings = {
            "invoice": self.invoice_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="transaction_id",
        )

    async def get_transactions(
        self,
        db_session: AsyncSession,
        user_id: Optional[UUID] = None,
        transaction_status: Optional[PaymentStatusEnum] = None,
        transaction_number: Optional[str] = None,
        invoice_number: Optional[str] = None,
        transaction_type: Optional[int] = None,
        amount_gte: Optional[float] = None,
        amount_lte: Optional[float] = None,
        date_gte: Optional[datetime] = None,
        date_lte: Optional[datetime] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            # Alias for Invoice model to ensure explicit join
            Invoice = aliased(self.invoice_dao.model)
            query = select(self.model).outerjoin(
                Invoice, self.model.invoice_number == Invoice.invoice_number
            )

            # Create a mapping for dynamic filter conditions
            filter_conditions = {
                "user_id": or_(
                    self.model.client_offered == user_id,
                    self.model.client_requested == user_id,
                )
                if user_id
                else None,
                "transaction_status": self.model.transaction_status
                == transaction_status
                if transaction_status
                else None,
                "transaction_number": self.model.transaction_number
                == transaction_number
                if transaction_number
                else None,
                "invoice_number": self.model.invoice_number == invoice_number
                if invoice_number
                else None,
                "transaction_type": self.model.transaction_type == transaction_type
                if transaction_type
                else None,
                "amount_gte": self.invoice_model.invoice_amount >= amount_gte
                if amount_gte is not None
                else None,
                "amount_lte": self.invoice_model.invoice_amount <= amount_lte
                if amount_lte is not None
                else None,
                "date_gte": self.model.transaction_date >= date_gte
                if date_gte
                else None,
                "date_lte": self.model.transaction_date <= date_lte
                if date_lte
                else None,
            }

            # Apply filters dynamically
            filters = [
                condition
                for condition in filter_conditions.values()
                if condition is not None
            ]
            if filters:
                query = query.where(*filters)

            query = query.limit(limit).offset(offset)
            result = await db_session.execute(query)
            transactions = result.scalars().all()
            # Build pagination metadata
            total_items = await db_session.execute(
                select(func.count()).select_from(query.subquery())
            )
            total_count = total_items.scalar()
            meta = {
                "total_items": total_count,
                "limit": limit,
                "offset": offset,
            }

            return DAOResponse(success=True, data=transactions, meta=meta)
        except Exception as e:
            raise CustomException(str(e))
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise CustomException(str(e))
