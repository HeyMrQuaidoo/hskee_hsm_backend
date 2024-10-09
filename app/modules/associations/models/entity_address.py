import uuid
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import Enum, UUID, Boolean, ForeignKey, CheckConstraint

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


# TODO (DQ): Deco concept of emergency hash in entity_address
# Remove primary key field
# - entity_id, address_id
class EntityAddress(Base):
    __tablename__ = "entity_address"

    entity_address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    entity_type: Mapped["EntityTypeEnum"] = mapped_column(Enum(EntityTypeEnum))
    address_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("address.address_id")
    )
    emergency_address: Mapped[bool] = mapped_column(
        Boolean, default=False, nullable=True
    )

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('property', 'user', 'pastrentalhistory', 'account', 'role')",
            name="check_entity_type_address",
        ),
    )

    __mapper_args__ = {"eager_defaults": True}

    @validates("entity_type", "entity_id")
    def validate_entity(self, key, value, **kwargs):
        if key == "entity_id":
            entity_id = value
            entity_type = kwargs.get("entity_type", self.entity_type)
        elif key == "entity_type":
            entity_type = value
            entity_id = self.entity_id

        entity_map = {
            EntityTypeEnum.property: (
                "property_unit_assoc",
                "property_unit_assoc_id",
            ),
            EntityTypeEnum.user: ("users", "user_id"),
            EntityTypeEnum.account: ("accounts", "account_id"),
            EntityTypeEnum.role: ("role", "role_id"),
            EntityTypeEnum.pastrentalhistory: (
                "past_rental_history",
                "rental_history_id",
            ),
        }

        if entity_type and EntityTypeEnum(str(entity_type)) in entity_map:
            super().validate_entity(
                entity_id=entity_id,
                entity_type=EntityTypeEnum(str(entity_type)),
                entity_map=entity_map,
            )
        return value
