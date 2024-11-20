from uuid import UUID
from typing import List
from fastapi import HTTPException, Depends
from sqlalchemy import and_, or_, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

# dao
from app.modules.communication.dao.message_dao import MessageDAO

# models
from app.modules.communication.models.message import Message

# routers
from app.modules.common.router.base_router import BaseCRUDRouter

# schema
from app.modules.common.schema.schemas import MessageSchema
from app.modules.communication.schema.calendar_event_schema import (
    CalendarEventCreateSchema,
    CalendarEventUpdateSchema,
    CalendarEventResponse,
)
from app.modules.communication.schema.message_schema import MessageCreate, MessageReply, MessageResponse
from app.core.response import DAOResponse
from app.modules.contract.models.under_contract import UnderContract
from app.modules.properties.models.property_unit_association import PropertyUnitAssoc
from app.modules.communication.models.message_recipient import MessageRecipient

# Core
class MessageRouter(BaseCRUDRouter):
    def __init__(self, prefix: str = "", tags: List[str] = []):
        self.dao: MessageDAO = MessageDAO(excludes=[])
        MessageSchema["create_schema"] = CalendarEventCreateSchema
        MessageSchema["update_schema"] = CalendarEventUpdateSchema
        MessageSchema["response_schema"] = CalendarEventResponse

        super().__init__(dao=self.dao, schemas=MessageSchema, prefix=prefix, tags=tags)
        self.register_routes()

    def register_routes(self):
        @self.router.post("/reply/")
        async def reply_to_message(
            message: MessageReply, db: AsyncSession = Depends(self.get_db)
        ):
            parent_message: Message = await self.dao.query(
                db_session=db,
                filters={"message_id": message.parent_message_id},
                single=True,
            )

            if not parent_message:
                raise HTTPException(status_code=404, detail="Parent message not found")

            return await self.dao.create(
                db_session=db,
                obj_in={
                    **message.model_dump(),
                    "subject": parent_message.subject,
                    "message_body": message.message_body,
                    "sender_id": message.sender_id,
                    "parent_message_id": message.parent_message_id,
                    "thread_id": parent_message.thread_id,
                },
            )

        @self.router.get(
            "/users/{user_id}/drafts",
            response_model=DAOResponse[List[MessageResponse]],
        )
        async def get_user_drafts(
            user_id: UUID, db: AsyncSession = Depends(self.get_db)
        ):
            messages: List[Message] = await self.dao.query(
                db_session=db,
                filters={
                    "sender_id": user_id,
                    "is_draft": True,
                    "is_scheduled": False,
                    "is_notification": False,
                },
            )

            return DAOResponse[List[MessageResponse]](
                success=True,
                data=[MessageResponse.model_validate(r) for r in messages],
            )

        @self.router.get(
            "/users/{user_id}/scheduled",
            response_model=DAOResponse[List[MessageResponse]],
        )
        async def get_user_scheduled(
            user_id: UUID, db: AsyncSession = Depends(self.get_db)
        ):
            messages: List[Message] = await self.dao.query(
                db_session=db,
                filters={
                    "sender_id": user_id,
                    "is_scheduled": True,
                    "is_draft": False,
                    "is_notification": False,
                },
            )

            return DAOResponse[List[MessageResponse]](
                success=True,
                data=[MessageResponse.model_validate(r) for r in messages],
            )

        @self.router.get(
            "/users/{user_id}/outbox",
            response_model=DAOResponse[List[MessageResponse]],
        )
        async def get_user_outbox(
            user_id: UUID, db: AsyncSession = Depends(self.get_db)
        ):
            messages: List[Message] = await self.dao.query(
                db_session=db,
                filters={
                    "sender_id": user_id,
                    "is_draft": False,
                    "is_scheduled": False,
                    "is_notification": False,
                },
                order_by=[desc(Message.date_created)],
            )

            return DAOResponse[List[MessageResponse]](
                success=True,
                data=[MessageResponse.model_validate(r) for r in messages],
            )

        @self.router.get(
            "/users/{user_id}/inbox",
            response_model=DAOResponse[List[MessageResponse]],
        )
        async def get_user_inbox(
            user_id: UUID, db: AsyncSession = Depends(self.get_db)
        ):
            # Asynchronously fetch the user's groups and contract dates
            user_contracts_stmt = (
                select(UnderContract)
                .join(
                    PropertyUnitAssoc,
                    PropertyUnitAssoc.property_unit_assoc_id
                    == UnderContract.property_unit_assoc_id,
                )
                .where(UnderContract.client_id == user_id)
            )
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
                    Message.is_notification is False,
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

        @self.router.get(
            "/users/{user_id}/notifications",
            response_model=DAOResponse[List[MessageResponse]],
        )
        async def get_user_notifications(
            user_id: UUID, db: AsyncSession = Depends(self.get_db)
        ):
            # Asynchronously fetch the user's groups and contract dates
            user_contracts_stmt = (
                select(UnderContract)
                .join(
                    PropertyUnitAssoc,
                    PropertyUnitAssoc.property_unit_assoc_id
                    == UnderContract.property_unit_assoc_id,
                )
                .where(UnderContract.client_id == user_id)
            )
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

