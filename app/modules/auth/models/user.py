import uuid
from typing import List, Optional
from datetime import date, datetime
from sqlalchemy.orm import relationship, Mapped, mapped_column
from sqlalchemy import UUID, Boolean, Date, DateTime, Enum, String, func, event

# enums
from app.modules.auth.enums.user_enums import GenderEnum

# models
from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


# TODO: Review assigned properties
class User(Base):
    __tablename__ = "users"

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    first_name: Mapped[str] = mapped_column(String(128))
    last_name: Mapped[str] = mapped_column(String(128))
    email: Mapped[str] = mapped_column(String(80), unique=True, index=True)
    phone_number: Mapped[str] = mapped_column(String(50))
    password: Mapped[str] = mapped_column(String(128), nullable=True)
    identification_number: Mapped[str] = mapped_column(String(80))
    photo_url: Mapped[str] = mapped_column(String(128))
    gender: Mapped["GenderEnum"] = mapped_column(Enum(GenderEnum))
    date_of_birth: Mapped[Optional[date]] = mapped_column(Date, nullable=True)

    # Authentication info
    login_provider: Mapped[str] = mapped_column(
        String(128), nullable=True, default="native"
    )
    reset_token: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    verification_token: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    is_subscribed_token: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    is_disabled: Mapped[bool] = mapped_column(Boolean, default=False)
    is_verified: Mapped[bool] = mapped_column(Boolean, default=True)
    is_subscribed: Mapped[bool] = mapped_column(Boolean, default=True)
    current_login_time: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True), default=func.now()
    )
    last_login_time: Mapped[Optional[DateTime]] = mapped_column(DateTime(timezone=True))

    # Employment info
    employer_name: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    occupation_status: Mapped[Optional[str]] = mapped_column(String(128), nullable=True)
    occupation_location: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )

    # Emergency Info
    emergency_contact_name: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    emergency_contact_email: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    emergency_contact_relation: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )
    emergency_contact_number: Mapped[Optional[str]] = mapped_column(
        String(128), nullable=True
    )

    # roles
    roles: Mapped[List["Role"]] = relationship(
        "Role", secondary="user_roles", back_populates="users", lazy="selectin"
    )

    # company
    company: Mapped[List["Company"]] = relationship(
        "Company",
        secondary="entity_company",
        secondaryjoin="and_(Company.company_id==EntityCompany.company_id, EntityCompany.entity_type=='user')",
        primaryjoin="and_(User.user_id==EntityCompany.entity_id)",
        back_populates="users",
    )

    # favorites
    favorites: Mapped["FavoriteProperties"] = relationship(
        "FavoriteProperties", back_populates="users", lazy="selectin"
    )

    # interactions
    interactions_as_user: Mapped[List["UserInteractions"]] = relationship(
        "UserInteractions",
        foreign_keys="[UserInteractions.user_id]",
        back_populates="user",
        lazy="selectin",
    )

    interactions_as_employee: Mapped[List["UserInteractions"]] = relationship(
        "UserInteractions",
        foreign_keys="[UserInteractions.employee_id]",
        back_populates="employee",
        lazy="selectin",
    )

    # address
    address: Mapped[List["Addresses"]] = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(User.user_id==EntityAddress.entity_id, EntityAddress.entity_type=='user')",
        secondaryjoin="and_(EntityAddress.address_id==Addresses.address_id, EntityAddress.emergency_address==False)",
        overlaps="address,entity_addresses,addresses,properties",
        back_populates="users",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # emergency_addresses
    emergency_addresses = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(User.user_id==EntityAddress.entity_id, EntityAddress.entity_type=='user')",
        secondaryjoin="and_(EntityAddress.address_id==Addresses.address_id, EntityAddress.emergency_address==True)",
        overlaps="address,entity_addresses,addresses,properties,rental_history",
        back_populates="users",
        lazy="selectin",
    )

    # accounts
    accounts: Mapped[List["Account"]] = relationship(
        "Account",
        secondary="entity_accounts",
        primaryjoin="and_(EntityAccount.entity_id==User.user_id, EntityAccount.entity_type=='user')",
        secondaryjoin="EntityAccount.account_id==Account.account_id",
        back_populates="users",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # documents
    documents: Mapped[List["Document"]] = relationship(
        "Document", back_populates="users", lazy="selectin"
    )

    # transactions
    transaction_as_client_offered: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="[Transaction.client_offered]",
        back_populates="client_offered_transaction",
        lazy="selectin",
    )

    transaction_as_client_requested: Mapped[List["Transaction"]] = relationship(
        "Transaction",
        foreign_keys="[Transaction.client_requested]",
        back_populates="client_requested_transaction",
        lazy="selectin",
    )

    # maintenance_requests
    maintenance_requests: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest", back_populates="user"
    )

    # tours
    tours: Mapped[List["TourBookings"]] = relationship("TourBookings", back_populates="user")

    # events
    events: Mapped[List["CalendarEvent"]] = relationship(
        "CalendarEvent", back_populates="organizer"
    )

    property_assignment: Mapped[List["PropertyAssignment"]] = relationship(
        "PropertyAssignment",
        foreign_keys="[PropertyAssignment.user_id]",
        back_populates="user",  # This matches the back_populates on PropertyAssignment
        lazy="selectin",
        viewonly=True,
    )

    # - messages
    sent_messages = relationship("Message", back_populates="sender", lazy="selectin")

    received_messages = relationship(
        "MessageRecipient", back_populates="recipient", lazy="selectin"
    )

    # - contracts
    client_under_contract: Mapped[List["UnderContract"]] = relationship(
        "UnderContract",
        foreign_keys="[UnderContract.client_id]",
        back_populates="client_representative",
        overlaps="members",
        lazy="selectin",
    )
    employee_under_contract: Mapped[List["UnderContract"]] = relationship(
        "UnderContract",
        foreign_keys="[UnderContract.employee_id]",
        back_populates="employee_representative",
        lazy="selectin",
    )

    # - rental history
    rental_history: Mapped[List["PastRentalHistory"]] = relationship(
        "PastRentalHistory",
        foreign_keys="[PastRentalHistory.user_id]",
        back_populates="user",
        lazy="selectin",
    )

    def update_last_login_time(self):
        # Store the current login time in the last_login_time field
        self.last_login_time = self.current_login_time

        # Update the current_login_time field to the current date
        self.current_login_time = datetime.now()

    def to_dict(self, exclude=["password"]):
        if exclude is None:
            exclude = set()
        data = {}

        for key in self.__dict__.keys():
            if not key.startswith("_") and key not in exclude:
                value = getattr(self, key)
                if isinstance(value, datetime):
                    value = str(value)
                if isinstance(value, UUID):
                    value = str(value)
                data[key] = value

        return data


def parse_date_of_birth(mapper, connection, target):
    """Listener to convert date_of_birth to a date if it's provided as a string."""
    if isinstance(target.date_of_birth, str):
        # (format 'YYYY-MM-DD')
        target.date_of_birth = datetime.strptime(
            target.date_of_birth, "%Y-%m-%d"
        ).date()


event.listen(User, "before_insert", parse_date_of_birth)
event.listen(User, "before_update", parse_date_of_birth)

# register model
Base.setup_model_dynamic_listener("user_roles", User)
