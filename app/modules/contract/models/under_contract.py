import uuid
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import DateTime, ForeignKey, Enum, UUID, String

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.contract.enums.contract_enums import ContractStatusEnum


# TODO (DQ):
# - start_date determined by contract.start_date
# - end_date determined by contract.end_date
# - next_payment_due should be determined by system
class UnderContract(Base):
    __tablename__ = "under_contract"

    under_contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property_unit_assoc.property_unit_assoc_id")
    )
    contract_status: Mapped[ContractStatusEnum] = mapped_column(
        Enum(ContractStatusEnum)
    )
    contract_number: Mapped[str] = mapped_column(
        String(128), ForeignKey("contract.contract_number", ondelete="CASCADE")
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )
    employee_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id"), nullable=True
    )
    start_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    end_date: Mapped[DateTime] = mapped_column(DateTime(timezone=True))
    next_payment_due: Mapped[DateTime] = mapped_column(DateTime(timezone=True))

    # properties
    properties: Mapped["PropertyUnitAssoc"] = relationship(
        "PropertyUnitAssoc", back_populates="under_contract", lazy="selectin"
    )

    # contract
    contract: Mapped["Contract"] = relationship(
        "Contract",
        back_populates="under_contract",
        lazy="selectin",
        foreign_keys=[contract_number],
        viewonly=True,
    )

    # users
    client_representative: Mapped["User"] = relationship(
        "User",
        foreign_keys=[client_id],
        back_populates="client_under_contract",
        lazy="selectin",
    )
    employee_representative: Mapped["User"] = relationship(
        "User",
        foreign_keys=[employee_id],
        back_populates="employee_under_contract",
        lazy="selectin",
    )
