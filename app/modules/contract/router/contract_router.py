from typing import List, Optional
from uuid import UUID
from fastapi import Depends, Query, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# DAO
from app.modules.contract.dao.contract_dao import ContractDAO

# Base CRUD Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import ContractSchema
from app.modules.contract.schema.contract_schema import (
    ContractCreateSchema,
    ContractUpdateSchema,
)

# Enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum

# Core
from app.core.lifespan import get_db
from app.core.response import DAOResponse
from app.core.errors import CustomException


class ContractRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: ContractDAO = ContractDAO(excludes=[])
        ContractSchema["create_schema"] = ContractCreateSchema
        ContractSchema["update_schema"] = ContractUpdateSchema
        # ContractSchema["response_schema"] = ContractResponse

        super().__init__(
            dao=self.dao,
            schemas=ContractSchema,
            prefix=prefix,
            tags=tags,
            route_overrides=["get_all"],
        )
        self.register_routes()

    def register_routes(self):
        @self.router.get("/")
        async def get_all_contracts(
            contract_number: Optional[str] = Query(None),
            contract_type_id: Optional[int] = Query(None),
            payment_type_id: Optional[int] = Query(None),
            contract_status: Optional[ContractStatusEnum] = Query(None),
            date_signed_gte: Optional[datetime] = Query(None),
            date_signed_lte: Optional[datetime] = Query(None),
            start_date_gte: Optional[datetime] = Query(None),
            start_date_lte: Optional[datetime] = Query(None),
            end_date_gte: Optional[datetime] = Query(None),
            end_date_lte: Optional[datetime] = Query(None),
            payment_amount_gte: Optional[float] = Query(None),
            payment_amount_lte: Optional[float] = Query(None),
            num_invoices: Optional[int] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_contracts(
                db_session=db_session,
                contract_number=contract_number,
                contract_type_id=contract_type_id,
                payment_type_id=payment_type_id,
                contract_status=contract_status,
                date_signed_gte=date_signed_gte,
                date_signed_lte=date_signed_lte,
                start_date_gte=start_date_gte,
                start_date_lte=start_date_lte,
                end_date_gte=end_date_gte,
                end_date_lte=end_date_lte,
                payment_amount_gte=payment_amount_gte,
                payment_amount_lte=payment_amount_lte,
                num_invoices=num_invoices,
                limit=limit,
                offset=offset,
            )

        @self.router.post(
            "/{contract_id}/upload_media", status_code=status.HTTP_201_CREATED
        )
        async def upload_media_to_contract(
            contract_id: UUID,
            files: List[UploadFile] = File(...),
            descriptions: List[str] = Form(None),
            captions: List[str] = Form(None),
            db_session: AsyncSession = Depends(get_db),
        ):
            try:
                await self.dao.upload_contract_media(
                    db_session=db_session,
                    contract_id=str(contract_id),
                    files=files,
                    descriptions=descriptions,
                    captions=captions,
                )
                return {"message": "Media uploaded successfully"}
            except Exception as e:
                raise CustomException(str(e))
