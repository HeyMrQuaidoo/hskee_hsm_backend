import uuid
from typing import List
from sqlalchemy import String, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Base model
from app.modules.billing.models.billable import BillableAssoc


class Utilities(BillableAssoc):
    __tablename__ = "utilities"

    billable_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("billable_assoc.billable_assoc_id"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(128), nullable=False)
    description: Mapped[str] = mapped_column(Text, nullable=True)

    __mapper_args__ = {
        "polymorphic_identity": "utilities",
    }

    # Relationships
    entity_billable: Mapped[List["EntityBillable"]] = relationship(
        "EntityBillable",
        back_populates="utility",
        lazy="selectin",
    )
