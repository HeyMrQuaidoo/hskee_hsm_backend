import uuid
import asyncio
from pydantic import ValidationError
from typing_extensions import override
from sqlalchemy.orm import selectinload
from typing import Dict, List, Optional, Union
from sqlalchemy.ext.asyncio import AsyncSession


# dao
from app.modules.auth.dao.role_dao import RoleDAO
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.billing.dao.account_dao import AccountDAO
from app.modules.address.dao.address_dao import AddressDAO
from app.modules.properties.dao.rental_history_dao import PastRentalHistoryDAO
from app.modules.properties.dao.property_assignment_dao import PropertyAssignmentDAO


# models
from app.modules.auth.models.user import User


# schemas
from app.modules.auth.schema.user_schema import UserCreateSchema

# core
from app.core.response import DAOResponse

# services
from app.services.email_service import EmailService
from app.core.config import settings
from app.core.security import Hash

UNSUBSCRIBE_LINK = "https://hskee-hsm-backend-test.onrender.com/auth/mail-unsubscribe?email={}&token={}"
VERIFICATION_LINK = (
    "https://hskee-hsm-backend-test.onrender.com/auth/verify-email?email={}&token={}"
)


class UserDAO(BaseDAO[User]):
    def __init__(self, excludes: Optional[List[str]] = []):
        self.model = User

        self.role_dao = RoleDAO()
        self.address_dao = AddressDAO()
        self.account_dao = AccountDAO()
        self.rental_history_dao = PastRentalHistoryDAO()
        self.detail_mappings = {
            "address": self.address_dao,
            "roles": self.role_dao,
            "rental_history": self.rental_history_dao,
            "accounts": self.account_dao,
            "property_assignment": PropertyAssignmentDAO(),
        }

        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="user_id",
        )

    @override
    async def create(
        self, db_session: AsyncSession, obj_in: Union[UserCreateSchema | Dict]
    ) -> DAOResponse:
        try:
            user_data = obj_in

            # check if user exists
            existing_user: User = await self.user_exists(
                db_session, user_data.model_dump().get("email")
            )

            if existing_user:
                raise Exception("User already exists")

            verification_token, is_subscribed_token = (
                str(uuid.uuid4()),
                str(uuid.uuid4()),
            )

            if "password" in user_data.model_dump():
                setattr(obj_in, "password", Hash.bcrypt(user_data.model_dump().get("password")))
            else:
                setattr(obj_in, "password", Hash.bcrypt(settings.APP_NAME))

            new_user: User = await super().create(
                db_session=db_session, obj_in=obj_in.model_dump()
            )

            # send email to user
            await self.send_verification_email(
                new_user, verification_token, is_subscribed_token
            )
            user_load_addr = await self.update_and_refresh_user(
                db_session, new_user, verification_token, is_subscribed_token
            )

            return (
                user_load_addr
                if isinstance(user_load_addr, DAOResponse)
                else user_load_addr
            )

        except ValidationError as e:
            raise e
        except Exception as e:
            await db_session.rollback()
            raise e

    async def user_exists(self, db_session: AsyncSession, email: str):
        return await self.query(
            db_session=db_session, filters={"email": email}, single=True
        )

    async def update_and_refresh_user(
        self,
        db_session: AsyncSession,
        user: User,
        verification_token: str,
        is_subscribed_token: str,
    ):
        """
        Updates the user's verification and subscription tokens and refreshes the session.
        """
        user_load_addr: User = await self.query(
            db_session=db_session,
            filters={f"{self.primary_key}": user.user_id},
            single=True,
            options=[selectinload(User.address)],
        )
        user.verification_token = verification_token
        user.is_subscribed_token = is_subscribed_token

        return await self.commit_and_refresh(db_session=db_session, obj=user_load_addr)

    async def send_verification_email(
        self, user: User, verification_token: str, is_subscribed_token: str
    ):
        """
        Sends a verification email to the user.
        """
        email_service = EmailService()
        asyncio.create_task(
            email_service.send_user_email(
                user.email,
                f"{user.first_name} {user.last_name}",
                VERIFICATION_LINK.format(user.email, verification_token),
                UNSUBSCRIBE_LINK.format(user.email, is_subscribed_token),
            )
        )
