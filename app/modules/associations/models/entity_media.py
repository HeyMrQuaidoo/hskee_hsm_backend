# app/modules/associations/models/entity_media.py

import uuid
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import Enum, CheckConstraint, UUID, ForeignKey

# Base model
from app.modules.common.models.model_base import BaseModel as Base

# Enums
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


class EntityMedia(Base):
    __tablename__ = "entity_media"

    entity_media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    media_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("media.media_id"), nullable=False
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    entity_type: Mapped[EntityTypeEnum] = mapped_column(Enum(EntityTypeEnum))
    media_type: Mapped[MediaType] = mapped_column(
        Enum(MediaType), default=MediaType.other
    )

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('property', 'user', 'units', 'amenities', 'entityamenities')",
            name="check_entity_type_media",
        ),
    )

    __mapper_args__ = {"eager_defaults": True}

    @validates("entity_id")
    def validate_entity(self, key, entity_id):
        entity_map = {
            EntityTypeEnum.user: ("users", "user_id"),
            EntityTypeEnum.amenities: ("amenities", "amenity_id"),
            EntityTypeEnum.property: ("property_unit_assoc", "property_unit_assoc_id"),
            EntityTypeEnum.entityamenities: ("entity_amenities", "entity_amenities_id"),
            EntityTypeEnum.units: ("property_unit", "property_unit_id"),
        }

        return super().validate_entity(
            entity_id=entity_id,
            entity_type=self.entity_type,
            entity_map=entity_map,
        )
