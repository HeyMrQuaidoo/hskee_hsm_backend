from typing import Optional, List
from uuid import UUID
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.response import DAOResponse
from app.modules.billing.dao.invoice_dao import InvoiceDAO
from app.modules.billing.dao.utility_dao import UtilityDAO
from app.modules.common.dao.base_dao import BaseDAO

# enums
from app.modules.contract.dao.under_contract_dao import UnderContractDAO
from app.modules.resources.dao.media_dao import MediaDAO
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum

# Models
from app.modules.contract.models.contract import Contract
from app.modules.resources.models.media import Media
from app.modules.associations.models.entity_media import EntityMedia

# Errors
from app.core.errors import CustomException, RecordNotFoundException

# Services
from fastapi import UploadFile
from app.services.upload_service import MediaUploaderService


class ContractDAO(BaseDAO[Contract]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Contract

        # DAOs for related entities
        self.under_contract_dao = UnderContractDAO()
        self.media_dao = MediaDAO()
        self.utility_dao = UtilityDAO()
        self.invoice_dao = InvoiceDAO()

        self.detail_mappings = {
            "media": self.media_dao,
            "utilities": self.utility_dao,
            "under_contract": self.under_contract_dao,
            "invoices": self.invoice_dao,
        }
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="contract_id",
        )

    async def get_contracts(
            self, db_session: AsyncSession, user_id: Optional[UUID], limit: int, offset: int
        ) -> DAOResponse:
            try:
                query = select(self.model)
                if user_id:
                    query = query.where(self.model.user_id == user_id)
                query = query.limit(limit).offset(offset)
                result = await db_session.execute(query)
                items = result.scalars().all()

                # Build pagination metadata
                total_items = await db_session.execute(select(func.count()).select_from(query.subquery()))
                total_count = total_items.scalar()
                meta = {
                    "total_items": total_count,
                    "limit": limit,
                    "offset": offset,
                }

                return DAOResponse(success=True, data=items, meta=meta)
            except Exception as e:
                raise CustomException(str(e))

    async def upload_contract_media(
        self,
        db_session: AsyncSession,
        contract_id: str,
        files: List[UploadFile],
        descriptions: Optional[List[str]],
        captions: Optional[List[str]],
    ):
        # Check if contract exists
        contract = await self.get(db_session=db_session, id=contract_id)
        if not contract:
            raise RecordNotFoundException(model="Contract", id=contract_id)

        for idx, file in enumerate(files):
            content = await file.read()
            base64_image = f"data:{file.content_type};base64,{content.decode('latin1')}"
            file_name = file.filename
            media_type = "contract"

            # Use MediaUploaderService
            uploader = MediaUploaderService(base64_image, file_name, media_type)
            response = uploader.upload()

            if not response.success:
                raise Exception(f"Upload failed: {response.error}")

            # Save media record and association
            media_data = {
                "media_name": file_name,
                "media_type": MediaType.document,  # Assuming documents for contracts
                "content_url": response.data["content_url"],
                "is_thumbnail": False,
                "caption": captions[idx] if captions and idx < len(captions) else None,
                "description": descriptions[idx]
                if descriptions and idx < len(descriptions)
                else None,
            }
            await self.add_media_to_contract(
                db_session=db_session,
                contract_id=contract_id,
                media_data=media_data,
            )

    async def add_media_to_contract(
        self,
        db_session: AsyncSession,
        contract_id: str,
        media_data: dict,
    ):
        # Create Media instance
        media = Media(**media_data)
        db_session.add(media)
        await db_session.flush()

        # Create EntityMedia association
        entity_media = EntityMedia(
            media_id=media.media_id,
            entity_id=contract_id,
            entity_type=EntityTypeEnum.contract,
            media_type=media.media_type,
        )
        db_session.add(entity_media)
        await db_session.commit()
