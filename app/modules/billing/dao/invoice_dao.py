from uuid import UUID
from datetime import datetime
from typing import Optional, List
from collections import defaultdict
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import and_, select, func, extract

from app.core.response import DAOResponse
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.billing.models.invoice import Invoice

# dao
from app.modules.billing.dao.invoice_item_dao import InvoiceItemDAO

# models

# core
from app.core.errors import CustomException, IntegrityError, RecordNotFoundException


class InvoiceDAO(BaseDAO[Invoice]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Invoice

        self.invoice_item_dao = InvoiceItemDAO()

        self.detail_mappings = {
            "invoice_items": self.invoice_item_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="invoice_number",
        )

    async def get_leases_due(
        self,
        db_session: AsyncSession,
        contract_type_name: str = CONTRACT_LEASE,
        user_id: str = None,
        offset=0,
        limit=100,
    ):
        filters = {
            "status": PaymentStatusEnum.pending.name,
            "ContractType.contract_type_name": contract_type_name,
            "Contract.contract_status": str(ContractStatusEnum.active.name),
            "UnderContract.contract_status": str(ContractStatusEnum.active.name),
        }

        join_conditions = [
            (ContractInvoice, ContractInvoice.invoice_number == Invoice.invoice_number),
            (Contract, Contract.contract_id == ContractInvoice.contract_id),
            (UnderContract, UnderContract.contract_id == Contract.contract_id),
            (ContractType, ContractType.contract_type_id == Contract.contract_type_id),
        ]

        if user_id:
            filters["UnderContract.client_id"] = UUID(user_id)

        options = [
            joinedload(Invoice.contracts),
            joinedload(Invoice.transaction),
            joinedload(Invoice.invoice_items),
        ]
        query_result = await self.query_on_joins(
            db_session=db_session,
            filters=filters,
            join_conditions=join_conditions,
            options=options,
            skip=offset,
            limit=limit,
        )

        return DAOResponse[List[InvoiceDueResponse]](
            success=True,
            data=[InvoiceDueResponse.from_orm_model(r) for r in query_result],
        )

    async def get_invoice_trends(
        self,
        db_session: AsyncSession,
        month: Optional[int] = None,
        year: Optional[int] = None,
    ) -> dict:
        try:
            trends_data = {}
            print(f"Fetching invoice trends for month: {month}, year: {year}")

            # If month or year is specified, filter by specific month/year
            if month or year:
                print(f"Filtering by specific month/year: month={month}, year={year}")
                query = select(
                    func.sum(self.model.invoice_amount).label("total_amount"),
                    func.count(self.model.invoice_id).label("total_count"),
                )
                if month:
                    query = query.where(extract("month", self.model.due_date) == month)
                if year:
                    query = query.where(extract("year", self.model.due_date) == year)

                specific_result = await db_session.execute(query)
                specific_data = specific_result.fetchone()
                trends_data["filtered_data"] = {
                    "total_amount": float(specific_data.total_amount)
                    if specific_data.total_amount
                    else 0,
                    "total_count": specific_data.total_count or 0,
                    "month": month,
                    "year": year,
                }
            else:
                # Get total amount and count since inception
                print("Querying total amount and count since inception")
                total_query = select(
                    func.sum(self.model.invoice_amount).label("total_amount"),
                    func.count(self.model.invoice_id).label("total_count"),
                )
                total_result = await db_session.execute(total_query)
                total_data = total_result.fetchone()
                trends_data["total_since_inception"] = {
                    "total_amount": float(total_data.total_amount)
                    if total_data.total_amount
                    else 0,
                    "total_count": total_data.total_count or 0,
                }

                # Get month-by-month trends
                print("Querying month-by-month trends")
                month_query = (
                    select(
                        extract("year", self.model.due_date).label("year"),
                        extract("month", self.model.due_date).label("month"),
                        func.sum(self.model.invoice_amount).label("total_amount"),
                        func.count(self.model.invoice_id).label("total_count"),
                    )
                    .group_by("year", "month")
                    .order_by("year", "month")
                )
                month_result = await db_session.execute(month_query)
                month_trends = defaultdict(
                    lambda: defaultdict(lambda: {"total_amount": 0, "total_count": 0})
                )

                for yr, mo, total_amount, total_count in month_result:
                    month_trends[int(yr)][int(mo)] = {
                        "total_amount": float(total_amount) if total_amount else 0,
                        "total_count": total_count or 0,
                    }
                trends_data["month_by_month"] = month_trends

                # Get year-by-year trends
                print("Querying year-by-year trends")
                year_query = (
                    select(
                        extract("year", self.model.due_date).label("year"),
                        func.sum(self.model.invoice_amount).label("total_amount"),
                        func.count(self.model.invoice_id).label("total_count"),
                    )
                    .group_by("year")
                    .order_by("year")
                )
                year_result = await db_session.execute(year_query)
                year_trends = {
                    int(yr): {
                        "total_amount": float(total_amount) if total_amount else 0,
                        "total_count": total_count or 0,
                    }
                    for yr, total_amount, total_count in year_result
                }
                trends_data["year_by_year"] = year_trends

            print(f"Final trends data: {trends_data}")
            return DAOResponse(success=True, data=trends_data)

        except RecordNotFoundException as e:
            raise e
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise CustomException(str(e))

    async def filter_invoices(
        self,
        db_session: AsyncSession,
        invoice_number: Optional[str] = None,
        issued_by: Optional[UUID] = None,
        issued_to: Optional[UUID] = None,
        invoice_type: Optional[str] = None,
        status: Optional[str] = None,
        min_amount: Optional[float] = None,
        max_amount: Optional[float] = None,
        due_date_from: Optional[datetime] = None,
        due_date_to: Optional[datetime] = None,
    ) -> List[Invoice]:
        try:
            print(
                f"Incoming parameters - invoice_number: {invoice_number}, issued_by: {issued_by}, issued_to: {issued_to}, "
                f"invoice_type: {invoice_type}, status: {status}, min_amount: {min_amount}, max_amount: {max_amount}, "
                f"due_date_from: {due_date_from}, due_date_to: {due_date_to}"
            )

            query = select(self.model)

            # Use a mapping to dynamically construct filters
            filter_conditions = {
                "invoice_number": self.model.invoice_number == invoice_number
                if invoice_number
                else None,
                "issued_by": self.model.issued_by == issued_by if issued_by else None,
                "issued_to": self.model.issued_to == issued_to if issued_to else None,
                "invoice_type": self.model.invoice_type == invoice_type
                if invoice_type
                else None,
                "status": self.model.status == status if status else None,
                "min_amount": self.model.invoice_amount >= min_amount
                if min_amount is not None
                else None,
                "max_amount": self.model.invoice_amount <= max_amount
                if max_amount is not None
                else None,
                "due_date_from": self.model.due_date >= due_date_from
                if due_date_from
                else None,
                "due_date_to": self.model.due_date <= due_date_to
                if due_date_to
                else None,
            }

            # Filter out None values and apply conditions
            filters = [
                condition
                for condition in filter_conditions.values()
                if condition is not None
            ]
            if filters:
                query = query.where(and_(*filters))

            result = await db_session.execute(query)
            return result.scalars().all()
        except RecordNotFoundException as e:
            raise e
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise CustomException(str(e))
