from typing import List
import uuid
from sqlalchemy import String, Text, UUID, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from typing import List

# Base model
from app.modules.billing.models.billable import BillableAssoc


class Utilities(BillableAssoc):
    __tablename__ = "utilities"

    utility_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

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

    # Properties
    properties: Mapped[List["Property"]] = relationship(
        "Property",
        secondary="entity_billable",
        primaryjoin="and_(Utilities.billable_assoc_id == EntityBillable.billable_id, EntityBillable.billable_type == 'utilities')",
        secondaryjoin="EntityBillable.entity_id == Property.property_unit_assoc_id",
        back_populates="utilities",
        overlaps="entity_billables,entity_billable",
        lazy="selectin",
    )

    # Entity Billables
    # entity_billable: Mapped[List["EntityBillable"]] = relationship(
    #     "EntityBillable",
    #     back_populates="utility",
    #     overlaps="entity_billable,utilities",
    #     lazy="selectin",
    # )

    # Contracts
    # contracts: Mapped[List["Contract"]] = relationship(
    #     "Contract",
    #     secondary="entity_billable",
    #     primaryjoin="and_(Utilities.billable_assoc_id == EntityBillable.billable_id, EntityBillable.billable_type == 'utilities', EntityBillable.entity_type == 'contract')",
    #     secondaryjoin="EntityBillable.entity_id == Contract.contract_id",
    #     back_populates="utilities",
    #     overlaps="entity_billables,entity_billable",
    #     lazy="selectin",
    # )
