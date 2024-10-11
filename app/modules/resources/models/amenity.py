import uuid
from typing import List, Optional
from sqlalchemy import String, Text, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# Base model
from app.modules.common.models.model_base import BaseModel as Base

class Amenities(Base):
    __tablename__ = "amenities"

    amenity_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    amenity_name: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    amenity_short_name: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    properties: Mapped[List["Property"]] = relationship(
        "Property",
        secondary="entity_amenities",
        primaryjoin="Amenities.amenity_id == EntityAmenities.amenity_id",
        secondaryjoin="and_(EntityAmenities.entity_id == Property.property_unit_assoc_id, EntityAmenities.entity_type == 'property')",
        back_populates="amenities",
        lazy="selectin",
    )

# Register model
Base.setup_model_dynamic_listener("amenities", Amenities)
