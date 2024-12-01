# from uuid import UUID
# from typing import List
# from fastapi import HTTPException, Depends
# from sqlalchemy import and_, or_, select, desc
# from sqlalchemy.ext.asyncio import AsyncSession

# # dao
# from app.modules.communication.dao.message_dao import MessageDAO

# # models
# from app.modules.communication.models.message import Message

# # routers
# from app.modules.common.router.base_router import BaseCRUDRouter

# # schema
# from app.modules.common.schema.schemas import MessageSchema
# from app.modules.communication.schema.calendar_event_schema import (
#     CalendarEventCreateSchema,
#     CalendarEventUpdateSchema,
#     CalendarEventResponse,
# )
# from app.modules.communication.schema.message_schema import MessageCreate, MessageReplySchema, MessageResponse
# from app.core.response import DAOResponse
# from app.modules.contract.models.under_contract import UnderContract
# from app.modules.properties.models.property_unit_association import PropertyUnitAssoc
# from app.modules.communication.models.message_recipient import MessageRecipient

# # Core
# class MessageRouter(BaseCRUDRouter):
#     def __init__(self, prefix: str = "", tags: List[str] = []):
#         self.dao: MessageDAO = MessageDAO(excludes=[])
#         MessageSchema["create_schema"] = CalendarEventCreateSchema
#         MessageSchema["update_schema"] = CalendarEventUpdateSchema
#         MessageSchema["response_schema"] = CalendarEventResponse


from typing import List
from pydantic import UUID4
from fastapi import Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

# DAO
from app.modules.communication.dao.message_dao import MessageDAO

# Router
from app.modules.common.router.base_router import BaseCRUDRouter

# Schemas
from app.modules.common.schema.schemas import MessageSchema
from app.modules.communication.schema.message_schema import (
    MessageCreateSchema,
    # MessageUpdateSchema,
    MessageReplySchema,
)


# Core
from app.core.lifespan import get_db


class MessageRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: MessageDAO = MessageDAO(excludes=[])
        MessageSchema["create_schema"] = MessageCreateSchema
        # Message["update_schema"] = MessageUpdateSchema

        super().__init__(
            dao=self.dao,
            schemas=MessageSchema,
            prefix=prefix,
            tags=tags,
        )
        self.register_routes()

    def register_routes(self):
        @self.router.post("/reply/")
        async def reply_to_message(
            message: MessageReplySchema, db_session: AsyncSession = Depends(get_db)
        ):
            result = await self.dao.reply_to_message(
                db_session=db_session, message=message
            )
            if not result.success:
                raise HTTPException(status_code=400, detail=result.error)
            return result

        @self.router.get("/users/{user_id}/drafts")
        async def get_user_drafts(
            user_id: UUID4,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ):
            return await self.dao.get_user_messages(
                db_session=db_session,
                user_id=user_id,
                folder="drafts",
                limit=limit,
                offset=offset,
            )

        @self.router.get("/users/{user_id}/scheduled")
        async def get_user_scheduled(
            user_id: UUID4,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ):
            return await self.dao.get_user_messages(
                db_session=db_session,
                user_id=user_id,
                folder="scheduled",
                limit=limit,
                offset=offset,
            )

        @self.router.get("/users/{user_id}/outbox")
        async def get_user_outbox(
            user_id: UUID4,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ):
            return await self.dao.get_user_messages(
                db_session=db_session,
                user_id=user_id,
                folder="outbox",
                limit=limit,
                offset=offset,
            )

        @self.router.get("/users/{user_id}/inbox")
        async def get_user_inbox(
            user_id: UUID4,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ):
            return await self.dao.get_user_messages(
                db_session=db_session,
                user_id=user_id,
                folder="inbox",
                limit=limit,
                offset=offset,
            )

        @self.router.get("/users/{user_id}/notifications")
        async def get_user_notifications(
            user_id: UUID4,
            limit: int = Query(default=10, ge=1),
            offset: int = Query(default=0, ge=0),
            db_session: AsyncSession = Depends(get_db),
        ):
            return await self.dao.get_user_messages(
                db_session=db_session,
                user_id=user_id,
                folder="notifications",
                limit=limit,
                offset=offset,
            )
