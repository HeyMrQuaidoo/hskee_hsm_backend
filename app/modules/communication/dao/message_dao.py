from uuid import UUID
from typing_extensions import override
from sqlalchemy.orm.exc import NoResultFound
from typing import Any, List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession

# daos
from app.modules.common.dao.base_dao import BaseDAO

# utils
from app.core.config import settings
from app.core.response import DAOResponse

# models
from app.modules.communication.models.message import Message
from app.modules.communication.models.message_recipient import MessageRecipient

# schemas
from app.modules.communication.schema.message_schema import (
    MessageCreate,
    MessageResponse,
)

EMAIL = settings.EMAIL
EMAIL_PASSWORD = settings.EMAIL_PASSWORD
SERVER = settings.EMAIL_SERVER


class MessageDAO(BaseDAO[Message]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Message
        self.detail_mappings = {}

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes or [],
            primary_key="message_id",
        )

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: MessageCreate
    ) -> DAOResponse[MessageResponse]:
        try:
            obj_in: dict = obj_in
            message_items = {
                key: value
                for key, value in obj_in.items()
                if key not in ["recipient_ids", "recipient_groups"]
            }

            # extract base information
            message_info = self.extract_model_data(message_items, MessageCreate)

            # create new user
            new_message: Message = await super().create(
                db_session=db_session, obj_in=message_info
            )
            new_message.thread_id = new_message.message_id
            new_message.parent_message_id = new_message.message_id

            # Create and add message recipients
            recipients = [
                MessageRecipient(
                    recipient_id=rid, message_id=new_message.message_id, is_read=False
                )
                for rid in obj_in["recipient_ids"]
            ]
            recipients_groups = [
                MessageRecipient(
                    recipient_group_id=rid,
                    message_id=new_message.message_id,
                    is_read=False,
                )
                for rid in obj_in["recipient_groups"]
            ]
            db_session.add_all(recipients + recipients_groups)

            # commit transactions.
            for obj in recipients + recipients_groups:
                await self.commit_and_refresh(db_session=db_session, obj=obj)

            await self.commit_and_refresh(db_session=db_session, obj=new_message)
            return DAOResponse[MessageResponse](
                success=True, data=MessageResponse.model_validate(new_message)
            )
        except NoResultFound:
            msg = "MessageDAO Create Failure"
            return DAOResponse(success=False, error=msg)
        except Exception as e:
            await db_session.rollback()
            msg = f"MessageDAO Create Failure: {str(e)}"
            return DAOResponse(success=False, error=msg)

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
