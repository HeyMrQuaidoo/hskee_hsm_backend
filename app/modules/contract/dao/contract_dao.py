# app/modules/contract/dao/contract_dao.py

from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.modules.common.dao.base_dao import BaseDAO

# Models
from app.modules.contract.models.contract import Contract
from app.modules.resources.models.media import Media
from app.modules.associations.models.entity_media import EntityMedia
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum
from app.modules.resources.enums.resource_enums import MediaType

# Enums
from app.modules.associations.enums.user_role_enums import UserRoleEnum

# Errors
from app.core.errors import RecordNotFoundException

# Services
from app.services.upload_service import MediaUploaderService
from fastapi import UploadFile

class ContractDAO(BaseDAO[Contract]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Contract
        self.detail_mappings = {
            "assigned_users": "ContractAssignment",
            "media": "Media",
        }
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="contract_id",
        )

    # Existing methods...

    async def upload_media_to_contract(
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
                "description": descriptions[idx] if descriptions and idx < len(descriptions) else None,
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
