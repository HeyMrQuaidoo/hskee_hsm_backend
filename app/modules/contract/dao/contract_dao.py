from typing import Optional, List
from uuid import UUID
from sqlalchemy import func, select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

# DAOs
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.contract.dao.under_contract_dao import UnderContractDAO
from app.modules.resources.dao.media_dao import MediaDAO
from app.modules.billing.dao.utility_dao import UtilityDAO
from app.modules.billing.dao.invoice_dao import InvoiceDAO

# Models
from app.modules.contract.models.contract import Contract
from app.modules.contract.enums.contract_enums import ContractStatusEnum
from app.modules.resources.models.media import Media
from app.modules.associations.models.entity_media import EntityMedia

# Enums
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum

# Core
from app.core.response import DAOResponse
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
            primary_key="contract_number",
        )

    async def get_contracts(
        self,
        db_session: AsyncSession,
        contract_number: Optional[str] = None,
        contract_type_id: Optional[int] = None,
        payment_type_id: Optional[int] = None,
        contract_status: Optional[ContractStatusEnum] = None,
        date_signed_gte: Optional[datetime] = None,
        date_signed_lte: Optional[datetime] = None,
        start_date_gte: Optional[datetime] = None,
        start_date_lte: Optional[datetime] = None,
        end_date_gte: Optional[datetime] = None,
        end_date_lte: Optional[datetime] = None,
        payment_amount_gte: Optional[float] = None,
        payment_amount_lte: Optional[float] = None,
        num_invoices: Optional[int] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            query = select(self.model)

            filter_conditions = {
                "contract_number": self.model.contract_number.ilike(f"%{contract_number}%")
                if contract_number
                else None,
                "contract_type_id": self.model.contract_type_id == contract_type_id
                if contract_type_id
                else None,
                "payment_type_id": self.model.payment_type_id == payment_type_id
                if payment_type_id
                else None,
                "contract_status": self.model.contract_status == contract_status
                if contract_status
                else None,
                "date_signed_gte": self.model.date_signed >= date_signed_gte
                if date_signed_gte
                else None,
                "date_signed_lte": self.model.date_signed <= date_signed_lte
                if date_signed_lte
                else None,
                "start_date_gte": self.model.start_date >= start_date_gte
                if start_date_gte
                else None,
                "start_date_lte": self.model.start_date <= start_date_lte
                if start_date_lte
                else None,
                "end_date_gte": self.model.end_date >= end_date_gte
                if end_date_gte
                else None,
                "end_date_lte": self.model.end_date <= end_date_lte
                if end_date_lte
                else None,
                "payment_amount_gte": self.model.payment_amount >= payment_amount_gte
                if payment_amount_gte is not None
                else None,
                "payment_amount_lte": self.model.payment_amount <= payment_amount_lte
                if payment_amount_lte is not None
                else None,
                "num_invoices": self.model.num_invoices == num_invoices
                if num_invoices is not None
                else None,
            }

            filters = [
                condition for condition in filter_conditions.values() if condition is not None
            ]

            if filters:
                query = query.where(and_(*filters))

            query = query.order_by(self.model.contract_number.asc())

            total_query = select(func.count()).select_from(query.subquery())
            query = query.limit(limit).offset(offset)

            result = await db_session.execute(query)
            contracts = result.scalars().all()

            total_items_result = await db_session.execute(total_query)
            total_count = total_items_result.scalar()

            meta = {
                "total_items": total_count,
                "limit": limit,
                "offset": offset,
            }

            return DAOResponse(success=True, data=contracts, meta=meta)
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
            base64_content = f"data:{file.content_type};base64,{content.decode('latin1')}"
            file_name = file.filename
            media_type_str = "contract"

            # Use MediaUploaderService
            uploader = MediaUploaderService(base64_content, file_name, media_type_str)
            response = uploader.upload()

            if not response.success:
                raise Exception(f"Upload failed: {response.error}")

            # Determine media type based on file content type
            content_type = file.content_type
            if "image" in content_type:
                media_type = MediaType.image
            elif "video" in content_type:
                media_type = MediaType.video
            elif "audio" in content_type:
                media_type = MediaType.audio
            elif "application" in content_type:
                media_type = MediaType.document
            else:
                media_type = MediaType.other

            # Create Media instance
            media_data = {
                "media_name": file_name,
                "media_type": media_type,
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
