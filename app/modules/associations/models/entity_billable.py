import uuid
from sqlalchemy.orm import validates, relationship, Mapped, mapped_column
from sqlalchemy import (
    Boolean,
    Integer,
    Enum,
    CheckConstraint,
    Numeric,
    UUID,
    ForeignKey,
)

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.billing.enums.billing_enums import BillableTypeEnum
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


# TODO (DQ):
# - Add start period and end period for the billable item
# Remove primary key field
# - entity_type, entity_id, billable_id, billable_type
class EntityBillable(Base):
    __tablename__ = "entity_billable"

    entity_billable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    entity_type: Mapped[EntityTypeEnum] = mapped_column(Enum(EntityTypeEnum))

    payment_type_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("payment_type.payment_type_id")
    )
    billable_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("billable_assoc.billable_assoc_id")
    )
    billable_type: Mapped[BillableTypeEnum] = mapped_column(Enum(BillableTypeEnum))
    billable_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    apply_to_units: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('property', 'contract')",
            name="check_entity_type_billables",
        ),
    )

    # payment_type
    payment_type: Mapped["PaymentType"] = relationship(
        "PaymentType", back_populates="entity_billable", lazy="selectin"
    )

    # utilities
    utility: Mapped["Utilities"] = relationship("Utilities", lazy="selectin")

    @validates("entity_id")
    def validate_entity(self, entity_id):
        entity_map = {
            EntityTypeEnum.property: ("PropertyUnitAssoc", "property_unit_assoc_id"),
            EntityTypeEnum.contract: ("Contract", "contract_id"),
        }

        return super().validate_entity(
            entity_id=entity_id,
            entity_type=self.entity_type,
            entity_map=entity_map,
        )
