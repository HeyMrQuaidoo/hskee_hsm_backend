# message_dao.py

from uuid import UUID
from typing import List, Optional
from sqlalchemy import func, select, and_, or_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy.exc import IntegrityError

# DAO
from app.core.response import DAOResponse
from app.modules.common.dao.base_dao import BaseDAO

# Models
from app.modules.communication.models.message import Message
from app.modules.communication.models.message_recipient import MessageRecipient
from app.modules.contract.models.under_contract import UnderContract
from app.modules.properties.models.property_unit_association import PropertyUnitAssoc

# Schemas
from app.modules.communication.schema.message_schema import (
<<<<<<< HEAD
    MessageCreateSchema,
    MessageReplySchema,
=======
    MessageCreate,
>>>>>>> 89e297ba52136afaf7ef590cc9e8f72bf6f7e521
    MessageResponse,
)

# Core
from app.core.errors import CustomException, RecordNotFoundException

class MessageDAO(BaseDAO[Message]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Message
<<<<<<< HEAD

        # Initialize DAOs for related entities if necessary
        self.detail_mappings = {
            # "sender": UserDAO(),
            # "recipients": UserDAO(),
        }
=======
        self.detail_mappings = {}
>>>>>>> 89e297ba52136afaf7ef590cc9e8f72bf6f7e521

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="message_id",
        )

    async def create(
<<<<<<< HEAD
        self, db_session: AsyncSession, obj_in: MessageCreateSchema
    ) -> DAOResponse:
=======
        self, db_session: AsyncSession, obj_in: MessageCreate
    ) -> DAOResponse[MessageResponse]:
>>>>>>> 89e297ba52136afaf7ef590cc9e8f72bf6f7e521
        try:
            message_data = obj_in.dict(exclude_unset=True)
            recipient_ids = message_data.pop("recipient_ids", [])
            recipient_groups = message_data.pop("recipient_groups", [])

            new_message = Message(**message_data)
            db_session.add(new_message)
            await db_session.flush()

            # Setting thread_id and parent_message_id if not set
            if not new_message.thread_id:
                new_message.thread_id = new_message.message_id
            if not new_message.parent_message_id:
                new_message.parent_message_id = new_message.message_id

            # Creating and adding message recipients
            recipients = [
                MessageRecipient(
                    recipient_id=rid, message_id=new_message.message_id, is_read=False
                )
                for rid in recipient_ids
            ]
            recipients_groups = [
                MessageRecipient(
                    recipient_group_id=gid,
                    message_id=new_message.message_id,
                    is_read=False,
                )
                for gid in recipient_groups
            ]
            db_session.add_all(recipients + recipients_groups)
            await db_session.commit()

<<<<<<< HEAD
            # After committing, we have to now ensure the message with relationships are loaded
            stmt = (
                select(Message)
                .options(
                    selectinload(Message.sender),
                    selectinload(Message.recipients).selectinload(MessageRecipient.recipient),
                )
                .where(Message.message_id == new_message.message_id)
=======
            # commit transactions.
            for obj in recipients + recipients_groups:
                await self.commit_and_refresh(db_session=db_session, obj=obj)

            await self.commit_and_refresh(db_session=db_session, obj=new_message)
            return DAOResponse[MessageResponse](
                success=True, data=MessageResponse.model_validate(new_message)
>>>>>>> 89e297ba52136afaf7ef590cc9e8f72bf6f7e521
            )
            result = await db_session.execute(stmt)
            new_message_with_relationships = result.scalar_one()

            return DAOResponse(
                success=True, data=MessageResponse.model_validate(new_message_with_relationships)
            )
        except IntegrityError as e:
            await db_session.rollback()
            raise CustomException(str(e))
        except Exception as e:
            await db_session.rollback()
            raise CustomException(str(e))

<<<<<<< HEAD
    async def reply_to_message(
        self, db_session: AsyncSession, message: MessageReplySchema
    ) -> DAOResponse:
        try:
            # Fetching the parent message
            parent_message_result = await db_session.execute(
                select(self.model)
                .options(
                    selectinload(Message.sender),
                    selectinload(Message.recipients).selectinload(MessageRecipient.recipient),
                )
                .where(self.model.message_id == message.parent_message_id)
            )
            parent_message = parent_message_result.scalar_one_or_none()
            if not parent_message:
                raise RecordNotFoundException(
                    model="Message", id=str(message.parent_message_id)
                )

            # Creating new message
            new_message_data = {
                "subject": parent_message.subject,
                "message_body": message.message_body,
                "sender_id": message.sender_id,
                "parent_message_id": message.parent_message_id,
                "thread_id": parent_message.thread_id,
                "recipient_ids": message.recipient_ids,
                "recipient_groups": message.recipient_groups,
                "is_draft": False,
                "is_scheduled": False,
                "is_notification": False,
            }
            print("Message Before:", new_message_data)
            new_message_schema = MessageReplySchema(**new_message_data)
            result = await self.create(db_session=db_session, obj_in=new_message_schema)
            print("Message After:", result)
            return result
        except Exception as e:
            await db_session.rollback()
            raise CustomException(str(e))

    async def get_user_messages(
        self,
        db_session: AsyncSession,
        user_id: UUID,
        folder: str,
        limit: int = 10,
        offset: int = 0,
    ) -> DAOResponse:
        try:
            if folder == "drafts":
                query = select(self.model).where(
                    self.model.sender_id == user_id,
                    self.model.is_draft == True,
                    self.model.is_scheduled == False,
                    self.model.is_notification == False,
                )
            elif folder == "scheduled":
                query = select(self.model).where(
                    self.model.sender_id == user_id,
                    self.model.is_scheduled == True,
                    self.model.is_draft == False,
                    self.model.is_notification == False,
                )
            elif folder == "outbox":
                query = select(self.model).where(
                    self.model.sender_id == user_id,
                    self.model.is_draft == False,
                    self.model.is_scheduled == False,
                    self.model.is_notification == False,
                ).order_by(desc(self.model.date_created))
            elif folder in ["inbox", "notifications"]:
                is_notification = folder == "notifications"

                # Fetch user's contracts
                user_contracts_stmt = (
                    select(UnderContract)
                    .join(
                        PropertyUnitAssoc,
                        PropertyUnitAssoc.property_unit_assoc_id
                        == UnderContract.property_unit_assoc_id,
                    )
                    .where(UnderContract.client_id == user_id)
                )
                contracts_result = await db_session.execute(user_contracts_stmt)
                contracts = contracts_result.scalars().all()
                contract_periods = [
                    (
                        contract.property_unit_assoc_id,
                        contract.start_date,
                        contract.end_date,
                    )
                    for contract in contracts
                ]

                # Preparing filters
                contract_ids = [cp[0] for cp in contract_periods]
                date_filters = [
                    and_(
                        MessageRecipient.msg_send_date >= cp[1],
                        MessageRecipient.msg_send_date <= cp[2],
                    )
                    for cp in contract_periods
                ]
                query = (
                    select(self.model)
                    .join(
                        MessageRecipient,
                        self.model.message_id == MessageRecipient.message_id,
                    )
                    .where(
                        self.model.is_draft == False,
                        self.model.is_scheduled == False,
                        self.model.is_notification == is_notification,
                        or_(
                            MessageRecipient.recipient_id == user_id,
                            and_(
                                MessageRecipient.recipient_group_id.in_(contract_ids),
                                or_(*date_filters) if date_filters else True,
                            ),
                        ),
                    )
                    .order_by(desc(self.model.date_created))
                )
            else:
                raise CustomException(f"Unknown folder type: {folder}")

            # Applying pagination
            total_query = select(func.count()).select_from(query.subquery())
            query = query.limit(limit).offset(offset)

            # Executing queries with relationships eagerly loaded
            query = query.options(
                selectinload(self.model.sender),
                selectinload(self.model.recipients).selectinload(MessageRecipient.recipient),
            )
            result = await db_session.execute(query)
            messages = result.scalars().all()

            # Get total count
            total_items_result = await db_session.execute(total_query)
            total_count = total_items_result.scalar()

            meta = {
                "total_items": total_count,
                "limit": limit,
                "offset": offset,
            }

            return DAOResponse(
                success=True,
                data=[MessageResponse.model_validate(m) for m in messages],
                meta=meta,
            )
        except Exception as e:
            await db_session.rollback()
            raise CustomException(str(e))
=======
    @override
    async def get_all(
        self, db_session: AsyncSession, offset=0, limit=100
    ) -> DAOResponse[List[MessageResponse]]:
        result = await super().get_all(
            db_session=db_session, offset=offset, limit=limit
        )

        return DAOResponse[List[MessageResponse]](
            success=True, data=[MessageResponse.model_validate(r) for r in result]
        )

    @override
    async def get(
        self, db_session: AsyncSession, id: Union[UUID | Any | int]
    ) -> DAOResponse[MessageResponse]:
        result: Message = await super().get(db_session=db_session, id=id)

        return DAOResponse[MessageResponse](
            success=bool(result),
            data={} if result is None else MessageResponse.model_validate(result),
        )
>>>>>>> 89e297ba52136afaf7ef590cc9e8f72bf6f7e521
