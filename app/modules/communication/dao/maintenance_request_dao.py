# app/modules/communication/dao/maintenance_request_dao.py

from datetime import datetime
from typing import Optional, List
from uuid import UUID
from fastapi import UploadFile
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Base DAO
from app.core.errors import RecordNotFoundException
from app.core.response import DAOResponse
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum
from app.modules.associations.models.entity_media import EntityMedia
from app.modules.common.dao.base_dao import BaseDAO

# DAO
from app.modules.communication.dao.calendar_event_dao import CalendarEventDAO
from app.modules.resources.dao.media_dao import MediaDAO

# Models
from app.modules.communication.models.maintenance_request import MaintenanceRequest
from app.modules.resources.enums.resource_enums import MediaType
from app.services.upload_service import MediaUploaderService

# Core
from app.core.errors import CustomException, IntegrityError, RecordNotFoundException


class MaintenanceRequestDAO(BaseDAO[MaintenanceRequest]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = MaintenanceRequest

        # DAO for calendar event
        self.calendar_event_dao = CalendarEventDAO()

        # DAOs for Media
        self.media_dao = MediaDAO()

        # Detail mappings for creating related entities
        self.detail_mappings = {
            "calendar_event": self.calendar_event_dao,
            "media": self.media_dao,
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="maintenance_request_id",
        )

    async def get_requests(
        self,
        db_session: AsyncSession,
        user_id: Optional[UUID] = None,
        status: Optional[str] = None,
        priority: Optional[str] = None,
        task_number: Optional[str] = None,
        scheduled_date_gte: Optional[datetime] = None,
        scheduled_date_lte: Optional[datetime] = None,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            query = select(self.model)

            # Create a mapping for dynamic filter conditions
            filter_conditions = {
                "user_id": self.model.requested_by == user_id if user_id else None,
                "status": self.model.status == status if status else None,
                "priority": self.model.priority == priority if priority else None,
                "task_number": self.model.task_number == task_number
                if task_number
                else None,
                "scheduled_date_gte": self.model.scheduled_date >= scheduled_date_gte
                if scheduled_date_gte
                else None,
                "scheduled_date_lte": self.model.scheduled_date <= scheduled_date_lte
                if scheduled_date_lte
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

            # Limit and offset for pagination
            query = query.limit(limit).offset(offset)
            result = await db_session.execute(query)
            items = result.scalars().all()

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

            return DAOResponse(success=True, data=items, meta=meta)
        except Exception as e:
            raise CustomException(str(e))
        except IntegrityError as e:
            raise e
        except Exception as e:
            raise CustomException(str(e))

    async def upload_request_media(
        self,
        db_session: AsyncSession,
        request_id: str,
        files: List[UploadFile],
        descriptions: Optional[List[str]],
        captions: Optional[List[str]],
    ):
        # Check if maintenance request exists
        maintenance_requests = await self.get(db_session=db_session, id=request_id)
        if not maintenance_requests:
            raise RecordNotFoundException(model="MaintenanceRequest", id=request_id)

        for idx, file in enumerate(files):
            content = await file.read()
            base64_data = f"data:{file.content_type};base64,{content.decode('latin1')}"
            file_name = file.filename
            media_type = MediaType.image  # Adjust based on the type of media

            # Use MediaUploaderService
            uploader = MediaUploaderService(base64_data, file_name, media_type)
            response = uploader.upload()

            if not response.success:
                raise Exception(f"Upload failed: {response.error}")

            # Save media record and association
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
            await self.add_media_to_request(
                db_session=db_session,
                request_id=request_id,
                media_data=media_data,
            )

    async def add_media_to_request(
        self,
        db_session: AsyncSession,
        request_id: str,
        media_data: dict,
    ):
        # Create Media instance
        media = self.media_dao.model(**media_data)
        db_session.add(media)
        await db_session.flush()

        # Create EntityMedia association
        entity_media = EntityMedia(
            media_id=media.media_id,
            entity_id=request_id,
            entity_type=EntityTypeEnum.maintenance_requests,
            media_type=media.media_type,
        )
        db_session.add(entity_media)
        await db_session.commit()
