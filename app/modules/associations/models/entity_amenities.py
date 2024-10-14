import uuid
from typing import List
from sqlalchemy import Boolean, Enum, UUID, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship, Mapped, mapped_column, validates

# models
from app.modules.common.models.model_base import BaseModel as Base

# enums
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum


# Remove primary key field
# - entity_type
class EntityAmenities(Base):
    __tablename__ = "entity_amenities"

    entity_amenities_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    amenity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("amenities.amenity_id")
    )
    entity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
    )
    entity_type: Mapped[EntityTypeEnum] = mapped_column(Enum(EntityTypeEnum))
    apply_to_units: Mapped[bool] = mapped_column(Boolean, default=False)

    __table_args__ = (
        CheckConstraint(
            "entity_type IN ('property')", name="check_entity_type_amenities"
        ),
    )
    # amenity
    amenity: Mapped["Amenities"] = relationship(
        "Amenities", overlaps="amenities", lazy="selectin"
    )

    # media
    media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary="entity_media",
        primaryjoin="EntityAmenities.entity_amenities_id == EntityMedia.entity_id",
        secondaryjoin="and_(EntityMedia.media_id == Media.media_id, EntityMedia.entity_type == 'entityamenities')",
        lazy="selectin",
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
    