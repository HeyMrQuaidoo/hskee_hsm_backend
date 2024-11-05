from uuid import UUID
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, Query, status, UploadFile, File, Form

# DAO
from app.core.response import DAOResponse
from app.modules.contract.dao.contract_dao import ContractDAO

# Base CRUD Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import ContractSchema
from app.modules.contract.schema.contract_schema import (
    ContractCreateSchema,
    ContractUpdateSchema,
    # ContractResponse,
)

# Core
from app.core.lifespan import get_db
from app.core.errors import CustomException


class ContractRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: ContractDAO = ContractDAO(excludes=[])
        ContractSchema["create_schema"] = ContractCreateSchema
        ContractSchema["update_schema"] = ContractUpdateSchema
        # ContractSchema["response_schema"] = ContractResponse

        super().__init__(dao=self.dao, schemas=ContractSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def add_get_route(self):
        @self.router.get("/")
        async def get_contracts(
            user_id: Optional[UUID] = Query(None),
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ) -> DAOResponse:
            return await self.dao.get_contracts(
                db_session=db_session, user_id=user_id, limit=limit, offset=offset
            )

    def register_routes(self):
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
