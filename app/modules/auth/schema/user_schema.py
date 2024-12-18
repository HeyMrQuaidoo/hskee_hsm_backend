from uuid import uuid4
from typing import Any, List, Optional, Union
from datetime import timedelta

from pydantic import ConfigDict, Field, model_validator

# models
from app.modules.auth.models.user import User as UserModel

# schemas
from app.modules.common.schema.base_schema import BaseFaker
from app.modules.billing.schema.account_schema import AccountBase
from app.modules.address.schema.address_mixin import AddressMixin
from app.modules.auth.schema.mixins.user_auth_schema import UserAuthInfo
from app.modules.auth.schema.mixins.user_mixin import (
    UserBase,
    UserHiddenFields,
    FavoritePropertiesBase,
)
from app.modules.auth.schema.mixins.user_employer_schema import (
    UserEmployerInfo,
)
from app.modules.properties.schema.rental_history_schema import (
    PastRentalHistoryResponse,
)
from app.modules.auth.schema.mixins.user_emergency_schema import (
    UserEmergencyInfo,
)
from app.modules.auth.schema.role_schema import RoleBase
from app.modules.auth.schema.company_schema import CompanyBase
from app.modules.communication.schema.tour_schema import TourBase
from app.modules.address.schema.address_schema import AddressBase
from app.modules.resources.schema.document_schema import DocumentBase

# from app.modules.billing.schema.transaction_schema import TransactionBase
from app.modules.communication.schema.calendar_event_schema import CalendarEventBase
from app.modules.communication.schema.maintenance_request_schema import (
    MaintenanceRequestBase,
)
from app.modules.properties.schema.rental_history_schema import (
    PastRentalHistoryBase,
    PastRentalHistory,
)
from app.modules.properties.schema.mixins.property_assignment_mixin import (
    PropertyAssignment,
    PropertyAssignmentBase,
    PropertyAssignmentMixin,
)
from app.modules.auth.schema.mixins.user_interactions_mixin import (
    UserInteractionsBase,
)


class UserSchema(UserBase):
    roles: Optional[List[RoleBase]] = []
    company: Optional[List[CompanyBase]] = []
    favorites: Optional[List[FavoritePropertiesBase]] = []
    interactions_as_user: Optional[List[UserInteractionsBase]] = []
    address: Optional[List[AddressBase]] = []
    accounts: Optional[List[AccountBase]] = []
    documents: Optional[List[DocumentBase]] = []
    # transactions_as_client_offered: Optional[List[TransactionBase]] = []
    # transactions_as_client_requested: Optional[List[TransactionBase]] = []
    maintenance_requests: Optional[List[MaintenanceRequestBase]] = []
    tours: Optional[List[TourBase]] = []
    events: Optional[List[CalendarEventBase]] = []
    property_assignment: Optional[List[PropertyAssignmentBase]] = []
    rental_history: Optional[
        Union[List[PastRentalHistoryBase] | List[PastRentalHistory]]
    ] = []


class UserResponse(UserHiddenFields, UserSchema):
    user_id: Optional[Any] = None
    user_auth_info: Optional[UserAuthInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    property_assignment_count: int = 0
    property_assignment: Optional[
        Union[List[PropertyAssignmentBase] | List[Any] | PropertyAssignmentBase]
    ] = []

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        # json_encoders={
        # date: lambda v: v.strftime("%Y-%m-%d") if v else None,
        # datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S") if v else None,
        # },
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number": "+123456789",
                "identification_number": "123456789",
                "gender": "male",
                "date_of_birth": "1985-05-20",
                "roles": [
                    {"name": "string", "alias": "string", "description": "string"}
                ],
                "user_emergency_info": {
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_email": "jane@example.com",
                    "emergency_contact_relation": "Spouse",
                    "emergency_contact_number": "+987654321",
                },
                "user_auth_info": {
                    "login_provider": "native",
                    "reset_token": "reset_test_token",
                    "verification_token": "abc123",
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "is_subscribed_token": "sub_test_token",
                    "current_login_time": "2023-09-15T12:00:00",
                    "last_login_time": "2023-09-10T12:00:00",
                },
                "user_employer_info": {
                    "employer_name": "TechCorp",
                    "occupation_status": "Full-time",
                    "occupation_location": "New York",
                },
            }
        },
    )

    @model_validator(mode="after")
    def flatten_nested_info(cls, values):
        # user_emergency_info
        if values.user_emergency_info:
            values.emergency_contact_name = (
                values.user_emergency_info.emergency_contact_name
            )
            values.emergency_contact_email = (
                values.user_emergency_info.emergency_contact_email
            )
            values.emergency_contact_relation = (
                values.user_emergency_info.emergency_contact_relation
            )
            values.emergency_contact_number = (
                values.user_emergency_info.emergency_contact_number
            )

        # user_auth_info
        if values.user_auth_info:
            values.login_provider = values.user_auth_info.login_provider
            values.reset_token = values.user_auth_info.reset_token
            values.verification_token = values.user_auth_info.verification_token
            values.is_subscribed_token = values.user_auth_info.is_subscribed_token
            values.is_disabled = values.user_auth_info.is_disabled
            values.is_verified = values.user_auth_info.is_verified
            values.is_subscribed = values.user_auth_info.is_subscribed
            values.current_login_time = values.user_auth_info.current_login_time
            values.last_login_time = values.user_auth_info.last_login_time

        # user_employer_info
        if values.user_employer_info:
            values.employer_name = values.user_employer_info.employer_name
            values.occupation_status = values.user_employer_info.occupation_status
            values.occupation_location = values.user_employer_info.occupation_location

        return values

    @classmethod
    def model_validate(cls, user: Union[UserModel | Any]):
        # user: UserModel = super().model_validate(user)

        return cls(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
            photo_url=user.photo_url,
            identification_number=user.identification_number,
            roles=user.roles,
            user_auth_info=UserAuthInfo.get_user_auth_info(user),
            user_emergency_info=UserEmergencyInfo.get_user_emergency_info(user),
            user_employer_info=UserEmployerInfo.get_user_employer_info(user),
            created_at=user.created_at,
            rental_history=[
                PastRentalHistoryResponse.model_validate(r) for r in user.rental_history
            ],
            address=AddressMixin.get_address_base(user.address),
            accounts=AccountBase.model_validate(user.accounts),
            # contracts=contracts,
            # contracts_count=len(contracts),
            property_assignment_count=len(user.property_assignment),
            property_assignment=PropertyAssignmentMixin.get_property_assignment_info(
                user.property_assignment
            ),
        ).model_dump(
            exclude_none=True,
            exclude_unset=True,
            exclude=[
                "emergency_contact_name",
                "emergency_contact_email",
                "emergency_contact_relation",
                "emergency_contact_number",
                "login_provider",
                "reset_token",
                "verification_token",
                "is_subscribed_token",
                "is_disabled",
                "is_verified",
                "is_subscribed",
                "current_login_time",
                "last_login_time",
                "employer_name",
                "occupation_status",
                "occupation_location",
            ],
        )


class UserCreateSchema(UserHiddenFields, UserSchema):
    user_auth_info: Optional[UserAuthInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None
    property_assignment_count: int = 0
    property_assignment: Optional[
        Union[
            List[PropertyAssignment]
            | List[PropertyAssignmentBase]
            | PropertyAssignment
            | PropertyAssignmentBase
        ]
    ] = []

    # Faker attrributes
    _start_date = BaseFaker.date_between(start_date="-2y", end_date="-1y")
    _date_of_birth = BaseFaker.date_between(start_date="-30y", end_date="-6y")
    _end_date = _start_date + timedelta(days=BaseFaker.random_int(min=30, max=365))
    _gender = BaseFaker.random_choices(["male", "female", "other"], length=1)
    _account_type = BaseFaker.random_choices(["billing", "general", "debit"], length=1)
    _job = BaseFaker.job()

    # Faker attributes for PropertyAssignment
    _property_type = BaseFaker.random_choices(
        ["residential", "commercial", "industrial"], length=1
    )
    _property_status = BaseFaker.random_choices(
        ["sold", "rent", "lease", "bought", "available", "unavailable"], length=1
    )
    _assignment_type = BaseFaker.random_choices(
        ["other", "handler", "landlord", "contractor"], length=1
    )
    _date_from = BaseFaker.date_time_between(start_date="-2y", end_date="now")
    _date_to = _date_from + timedelta(days=BaseFaker.random_int(min=30, max=365))
    _notes = BaseFaker.text(max_nb_chars=200)

    for_insertion: bool = Field(default=True, exclude=True)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        # json_encoders={
        # date: lambda v: v.strftime("%Y-%m-%d") if v else None,
        # datetime: lambda v: v.strftime("%Y-%m-%dT%H:%M:%S") if v else None,
        # },
        json_schema_extra={
            "example": {
                "first_name": BaseFaker.first_name(),
                "last_name": BaseFaker.last_name(),
                "email": BaseFaker.email(),
                "phone_number": "+123456789",
                "identification_number": "1234567890",
                "gender": _gender[0],
                "date_of_birth": _date_of_birth,
                "roles": [{"name": _job, "alias": _job, "description": _job}],
                "user_emergency_info": {
                    "emergency_contact_name": BaseFaker.name(),
                    "emergency_contact_email": BaseFaker.email(),
                    "emergency_contact_relation": "Spouse",
                    "emergency_contact_number": BaseFaker.phone_number(),
                    "address": [
                        {
                            "address_1": "46304 Latoya Street Apt. 705",
                            "address_2": "Unit 0871 Box 9668\nDPO AA 30695",
                            "address_postalcode": "",
                            "address_type": "billing",
                            "city": "Pinedatown",
                            "country": "Malta",
                            "emergency_address": True,
                            "primary": True,
                            "region": "Mississippi",
                        }
                    ],
                },
                "user_auth_info": {
                    "login_provider": "native",
                    "reset_token": str(uuid4()),
                    "verification_token": str(uuid4()),
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "is_subscribed_token": str(uuid4()),
                    "current_login_time": "2023-09-15T12:00:00",
                    "last_login_time": "2023-09-10T12:00:00",
                },
                "user_employer_info": {
                    "employer_name": BaseFaker.company(),
                    "occupation_status": "Full-time",
                    "occupation_location": BaseFaker.city(),
                },
                "rental_history": [
                    {
                        "start_date": _start_date,
                        "end_date": _end_date,
                        "property_owner_name": BaseFaker.name(),
                        "property_owner_email": BaseFaker.email(),
                        "property_owner_mobile": BaseFaker.phone_number(),
                        "address": [
                            {
                                "address_type": "billing",
                                "primary": True,
                                "address_1": "lines 1",
                                "address_2": "lines 2",
                                "city": "Tema",
                                "region": "Greater Accra",
                                "country": "Ghana",
                                "address_postalcode": "",
                                "emergency_address": False,
                            }
                        ],
                    }
                ],
                "address": [
                    {
                        "address_type": "billing",
                        "primary": True,
                        "address_1": "lines 1",
                        "address_2": "lines 2",
                        "city": "Tema",
                        "region": "Greater Accra",
                        "country": "Ghana",
                        "address_postalcode": "",
                        "emergency_address": False,
                    }
                ],
                "accounts": [
                    {
                        "account_branch_name": "Cruz PLC Branch",
                        "account_type": "general",
                        "address": [
                            {
                                "address_1": "46304 Latoya Street Apt. 705",
                                "address_2": "Unit 0871 Box 9668\nDPO AA 30695",
                                "address_postalcode": "",
                                "address_type": "billing",
                                "city": "Pinedatown",
                                "country": "Malta",
                                "emergency_address": False,
                                "primary": True,
                                "region": "Mississippi",
                            }
                        ],
                        "bank_account_name": "Maxwell, Hall and White Bank",
                        "bank_account_number": "GB38FYRR90680780656781",
                    }
                ],
                "property_assignment": [
                    {
                        "property_unit_assoc_id": "5afb1996-e135-470f-a267-8a937be11be8",
                        "assignment_type": _assignment_type[0],
                        "date_from": _date_from,
                        "date_to": _date_to,
                        "notes": _notes,
                    }
                ],
            }
        },
    )

    @model_validator(mode="after")
    def flatten_nested_info(cls, values: "UserCreateSchema"):
        # user_emergency_info
        if values.for_insertion:
            if values.user_emergency_info:
                values.emergency_contact_name = (
                    values.user_emergency_info.emergency_contact_name
                )
                values.emergency_contact_email = (
                    values.user_emergency_info.emergency_contact_email
                )
                values.emergency_contact_relation = (
                    values.user_emergency_info.emergency_contact_relation
                )
                values.emergency_contact_number = (
                    values.user_emergency_info.emergency_contact_number
                )
                values.address.extend(values.user_emergency_info.address)

            # user_auth_info
            if values.user_auth_info:
                values.login_provider = values.user_auth_info.login_provider
                values.reset_token = values.user_auth_info.reset_token
                values.verification_token = values.user_auth_info.verification_token
                values.is_subscribed_token = values.user_auth_info.is_subscribed_token
                values.is_disabled = values.user_auth_info.is_disabled
                values.is_verified = values.user_auth_info.is_verified
                values.is_subscribed = values.user_auth_info.is_subscribed
                values.current_login_time = values.user_auth_info.current_login_time
                values.last_login_time = values.user_auth_info.last_login_time

            # user_employer_info
            if values.user_employer_info:
                values.employer_name = values.user_employer_info.employer_name
                values.occupation_status = values.user_employer_info.occupation_status
                values.occupation_location = (
                    values.user_employer_info.occupation_location
                )

        return values

    @classmethod
    def model_validate(cls, user: UserModel, for_insertion=True):
        instance = cls(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
            photo_url=user.photo_url,
            identification_number=user.identification_number,
            roles=user.roles,
            user_auth_info=UserAuthInfo.get_user_auth_info(user),
            user_emergency_info=UserEmergencyInfo.get_user_emergency_info(user),
            user_employer_info=UserEmployerInfo.get_user_employer_info(user),
            created_at=user.created_at,
            rental_history=[
                PastRentalHistoryResponse.model_validate(r) for r in user.rental_history
            ],
            address=AddressMixin.get_address_base(user.address),
            accounts=AccountBase.model_validate(user.accounts),
            property_assignment_count=len(user.property_assignment),
            property_assignment=PropertyAssignmentMixin.get_property_assignment_info(
                user.property_assignment
            ),
            # contracts=contracts,
            # contracts_count=len(contracts),
            for_insertion=for_insertion,
        )

        return instance.model_dump(
            exclude=[
                "emergency_contact_name",
                "emergency_contact_email",
                "emergency_contact_relation",
                "emergency_contact_number",
                "login_provider",
                "reset_token",
                "verification_token",
                "is_subscribed_token",
                "is_disabled",
                "is_verified",
                "is_subscribed",
                "current_login_time",
                "last_login_time",
                "employer_name",
                "occupation_status",
                "occupation_location",
            ],
        )


class UserUpdateSchema(UserHiddenFields, UserSchema):
    user_auth_info: Optional[UserAuthInfo] = None
    user_employer_info: Optional[UserEmployerInfo] = None
    user_emergency_info: Optional[UserEmergencyInfo] = None

    _assignment_type = BaseFaker.random_choices(
        ["other", "handler", "landlord", "contractor"], length=1
    )
    _date_from = BaseFaker.date_time_between(start_date="-2y", end_date="now")
    _date_to = _date_from + timedelta(days=BaseFaker.random_int(min=30, max=365))
    _notes = BaseFaker.text(max_nb_chars=200)

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        use_enum_values=True,
        # json_encoders={date: lambda v: v.strftime("%Y-%m-%d") if v else None},
        json_schema_extra={
            "example": {
                "first_name": "John",
                "last_name": "Doe",
                "email": "john@example.com",
                "phone_number": "+123456789",
                "identification_number": "123456789",
                "gender": "male",
                "date_of_birth": "1985-05-20",
                "roles": [
                    {"name": "string", "alias": "string", "description": "string"}
                ],
                "user_emergency_info": {
                    "emergency_contact_name": "Jane Doe",
                    "emergency_contact_email": "jane@example.com",
                    "emergency_contact_relation": "Spouse",
                    "emergency_contact_number": "+987654321",
                },
                "user_auth_info": {
                    "login_provider": "native",
                    "reset_token": "reset_test_token",
                    "verification_token": "abc123",
                    "is_disabled": False,
                    "is_verified": True,
                    "is_subscribed": True,
                    "is_subscribed_token": "sub_test_token",
                    "current_login_time": "2023-09-15T12:00:00",
                    "last_login_time": "2023-09-10T12:00:00",
                },
                "user_employer_info": {
                    "employer_name": "TechCorp",
                    "occupation_status": "Full-time",
                    "occupation_location": "New York",
                },
                "property_assignment": [
                    {
                        "property_unit_assoc_id": "402c0deb-b978-40d6-a269-c690cbd99589",
                        "assignment_type": _assignment_type[0],
                        "date_from": _date_from,
                        "date_to": _date_to,
                        "notes": _notes,
                    }
                ],
            }
        },
    )

    @model_validator(mode="after")
    def flatten_nested_info(cls, values: "UserUpdateSchema"):
        # user_emergency_info
        if values.user_emergency_info:
            values.emergency_contact_name = (
                values.user_emergency_info.emergency_contact_name
            )
            values.emergency_contact_email = (
                values.user_emergency_info.emergency_contact_email
            )
            values.emergency_contact_relation = (
                values.user_emergency_info.emergency_contact_relation
            )
            values.emergency_contact_number = (
                values.user_emergency_info.emergency_contact_number
            )

        # user_auth_info
        if values.user_auth_info:
            values.login_provider = values.user_auth_info.login_provider
            values.reset_token = values.user_auth_info.reset_token
            values.verification_token = values.user_auth_info.verification_token
            values.is_subscribed_token = values.user_auth_info.is_subscribed_token
            values.is_disabled = values.user_auth_info.is_disabled
            values.is_verified = values.user_auth_info.is_verified
            values.is_subscribed = values.user_auth_info.is_subscribed
            values.current_login_time = values.user_auth_info.current_login_time
            values.last_login_time = values.user_auth_info.last_login_time

        # user_employer_info
        if values.user_employer_info:
            values.employer_name = values.user_employer_info.employer_name
            values.occupation_status = values.user_employer_info.occupation_status
            values.occupation_location = values.user_employer_info.occupation_location

        return values

    @classmethod
    def model_validate(cls, user: UserModel):
        return cls(
            user_id=user.user_id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            phone_number=user.phone_number,
            gender=user.gender,
            date_of_birth=user.date_of_birth,
            photo_url=user.photo_url,
            identification_number=user.identification_number,
            roles=user.roles,
            user_auth_info=UserAuthInfo.get_user_auth_info(user),
            user_emergency_info=UserEmergencyInfo.get_user_emergency_info(user),
            user_employer_info=UserEmployerInfo.get_user_employer_info(user),
            created_at=user.created_at,
            rental_history=[
                PastRentalHistoryResponse.model_validate(r) for r in user.rental_history
            ],
            address=AddressMixin.get_address_base(user.address),
            accounts=AccountBase.model_validate(user.accounts),
            property_assignment_count=len(user.property_assignment),
            property_assignment=PropertyAssignmentMixin.get_property_assignment_info(
                user.property_assignment
            ),
            # contracts=contracts,
            # contracts_count=len(contracts),
        ).model_dump(
            exclude=[
                "emergency_contact_name",
                "emergency_contact_email",
                "emergency_contact_relation",
                "emergency_contact_number",
                "login_provider",
                "reset_token",
                "verification_token",
                "is_subscribed_token",
                "is_disabled",
                "is_verified",
                "is_subscribed",
                "current_login_time",
                "last_login_time",
                "employer_name",
                "occupation_status",
                "occupation_location",
            ],
        )
