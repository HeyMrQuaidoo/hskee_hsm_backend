import uuid
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import UUID, Enum, ForeignKey, CheckConstraint

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.billing.enums.billing_enums import CompanyTypeEnum
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


# Remove primary key field
# - company_type, entity_id, entity_type
class EntityCompany(Base):
    __tablename__ = "entity_company"

    entity_company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    company_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("company.company_id")
    )
    company_type: Mapped[CompanyTypeEnum] = mapped_column(
        Enum(CompanyTypeEnum), default=CompanyTypeEnum.agency
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    entity_type: Mapped[EntityTypeEnum] = mapped_column(Enum(EntityTypeEnum))

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('property', 'user')", name="check_entity_type_company"
        ),
    )

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
        }

        if entity_type and EntityTypeEnum(str(entity_type)) in entity_map:
            super().validate_entity(
                entity_id=entity_id,
                entity_type=EntityTypeEnum(str(entity_type)),
                entity_map=entity_map,
            )
        return value
