from uuid import UUID
from datetime import datetime
from typing import Annotated, List, Optional
from pydantic import ConfigDict, EmailStr, constr

# schemas
from app.modules.common.schema.base_schema import BaseSchema
from app.modules.auth.schema.mixins.user_mixin import UserBase, UserBaseMixin

# model
from app.modules.communication.models.message import Message as MessageModel


class EmailBody(BaseSchema):
    """
    Model for representing the body of an email.

    Attributes:
        to (EmailStr): The recipient's email address.
        subject (str): The subject of the email.
        message (str): The body of the email.
    """

    to: EmailStr
    subject: Annotated[str, constr(max_length=255)]
    message: Annotated[str, constr(max_length=2000)]

    model_config = ConfigDict(from_attributes=True)


class MessageCreateSchema(BaseSchema):
    """
    Schema for creating a message.

    Attributes:
        subject (str): The subject of the message.
        message_body (str): The body of the message.
        sender_id (UUID): The unique identifier of the sender.
        is_draft (Optional[bool]): Indicates if the message is a draft.
        is_scheduled (Optional[bool]): Indicates if the message is scheduled.
        recipient_ids (Optional[List[UUID]]): List of recipient IDs.
        recipient_groups (Optional[List[UUID]]): List of recipient group IDs.
    """

    subject: Annotated[str, constr(max_length=255)]
    message_body: Annotated[str, constr(max_length=2000)]
    sender_id: UUID
    is_draft: Optional[bool] = False
    is_scheduled: Optional[bool] = False
    recipient_ids: Optional[List[UUID]] = None
    recipient_groups: Optional[List[UUID]] = None

    model_config = ConfigDict(from_attributes=True)


class MessageReplySchema(BaseSchema):
    """
    Schema for replying to a message.

    Attributes:
        message_body (str): The body of the reply message.
        sender_id (UUID): The unique identifier of the sender.
        parent_message_id (UUID): The unique identifier of the parent message.
        recipient_ids (Optional[List[UUID]]): List of recipient IDs.
        recipient_groups (Optional[List[UUID]]): List of recipient group IDs.
    """

    message_body: Annotated[str, constr(max_length=2000)]
    sender_id: UUID
    parent_message_id: UUID
    recipient_ids: Optional[List[UUID]] = None
    recipient_groups: Optional[List[UUID]] = None

    model_config = ConfigDict(from_attributes=True)


class MessageResponse(BaseSchema, UserBaseMixin):
    """
    Model for representing a message response.

    Attributes:
        message_id (Optional[UUID]): The unique identifier of the message.
        subject (Optional[str]): The subject of the message.
        sender (Optional[UserBase]): The sender of the message.
        recipients (Optional[List[UserBase]]): List of recipients of the message.
        message_body (Optional[str]): The body of the message.
        parent_message_id (Optional[UUID]): The unique identifier of the parent message.
        thread_id (Optional[UUID]): The unique identifier of the message thread.
        is_draft (Optional[bool]): Indicates if the message is a draft.
        is_notification (Optional[bool]): Indicates if the message is a notification.
        is_reminder (Optional[bool]): Indicates if the message is a reminder.
        is_scheduled (Optional[bool]): Indicates if the message is scheduled.
        is_read (Optional[bool]): Indicates if the message is read.
        date_created (Optional[datetime]): The date the message was created.
        scheduled_date (Optional[datetime]): The scheduled date for the message.
        next_remind_date (Optional[datetime]): The next reminder date for the message.
    """

    message_id: Optional[UUID] = None
    subject: Optional[Annotated[str, constr(max_length=255)]] = None
    sender: Optional[UserBase] = None
    recipients: Optional[List[UserBase]] = None
    message_body: Optional[Annotated[str, constr(max_length=2000)]] = None
    parent_message_id: Optional[UUID] = None
    thread_id: Optional[UUID] = None
    is_draft: Optional[bool] = False
    is_notification: Optional[bool] = False
    is_reminder: Optional[bool] = False
    is_scheduled: Optional[bool] = False
    is_read: Optional[bool] = False
    date_created: Optional[datetime] = None
    scheduled_date: Optional[datetime] = None
    next_remind_date: Optional[datetime] = None

    model_config = ConfigDict(
        from_attributes=True,
        use_enum_values=True,
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

    @classmethod
    def model_validate(cls, message: MessageModel) -> "MessageResponse":
        """
        Create a MessageResponseModel instance from an ORM model.

        Args:
            message (MessageModel): Message ORM model.

        Returns:
            MessageResponseModel: Message response object.
        """

        # get message recipients
        message_recipients = [
            cls.get_user_info(message_recipients.recipient)
            for message_recipients in message.recipients
        ]

        return cls(
            message_id=message.message_id,
            message_body=message.message_body,
            subject=message.subject,
            sender=message.sender,
            parent_message_id=message.parent_message_id,
            thread_id=message.thread_id,
            is_draft=message.is_draft,
            is_notification=message.is_notification,
            is_reminder=message.is_reminder,
            is_scheduled=message.is_scheduled,
            is_read=message.is_read,
            date_created=message.date_created,
            scheduled_date=message.scheduled_date,
            next_remind_date=message.next_remind_date,
            recipients=message_recipients,
        ).model_dump()