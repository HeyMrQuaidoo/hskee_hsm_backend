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





from typing import List, Optional
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
<<<<<<< HEAD
=======
from app.modules.communication.schema.message_schema import (
    MessageReply,
    MessageResponse,
)
from app.core.response import DAOResponse
from app.modules.contract.models.under_contract import UnderContract
from app.modules.properties.models.property_unit_association import PropertyUnitAssoc
from app.modules.communication.models.message_recipient import MessageRecipient
>>>>>>> 89e297ba52136afaf7ef590cc9e8f72bf6f7e521


# Core
from app.core.lifespan import get_db
from app.core.response import DAOResponse

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
            result = await self.dao.reply_to_message(db_session=db_session, message=message)
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
<<<<<<< HEAD
=======
            contracts_result = await db.execute(user_contracts_stmt)
            contracts = contracts_result.scalars().all()
            contract_periods = [
                (
                    contract.property_unit_assoc_id,
                    contract.start_date,
                    contract.end_date,
                )
                for contract in contracts
            ]

            # Construct a list of group IDs for use in the next query
            if not contract_periods:
                contract_periods = []

            # Filter messages based on whether the send date is within any of the contract periods
            inbox_stmt = (
                select(Message)
                .join(
                    MessageRecipient, Message.message_id == MessageRecipient.message_id
                )
                .where(
                    Message.is_draft is False,
                    Message.is_scheduled is False,
                    Message.is_notification is True,
                    or_(
                        MessageRecipient.recipient_id == user_id,
                        and_(
                            MessageRecipient.recipient_group_id.in_(
                                [cp[0] for cp in contract_periods]
                            ),
                            or_(
                                *[
                                    and_(
                                        MessageRecipient.msg_send_date >= cp[1],
                                        MessageRecipient.msg_send_date <= cp[2],
                                    )
                                    for cp in contract_periods
                                ]
                            ),
                        ),
                    ),
                )
                .order_by(Message.date_created.desc())
            )
            inbox_messages_result = await db.execute(inbox_stmt)
            inbox_messages = inbox_messages_result.scalars().all()

            return DAOResponse[List[MessageResponse]](
                success=True,
                data=[MessageResponse.model_validate(r) for r in inbox_messages],
            )
>>>>>>> 89e297ba52136afaf7ef590cc9e8f72bf6f7e521
