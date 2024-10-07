import uuid
from sqlalchemy.orm import Mapped, mapped_column, validates
from sqlalchemy import Enum, CheckConstraint, UUID, ForeignKey

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


# Remove primary key field
# - media_type, entity_id, entity_type
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

    @validates("entity_id")
    def validate_entity(self, entity_id):
        entity_map = {
            EntityTypeEnum.user: ("User", "user_id"),
            EntityTypeEnum.amenities: ("Amenities", "amenity_id"),
            EntityTypeEnum.property: ("PropertyUnitAssoc", "property_unit_assoc_id"),
            EntityTypeEnum.entityamenities: ("EntityAmenities", "entity_amenities_id"),
        }

        return super().validate_entity(
            entity_id=entity_id,
            entity_type=self.entity_type,
            entity_map=entity_map,
        )
