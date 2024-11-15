import uuid
from typing import List
from datetime import datetime
from sqlalchemy.orm import relationship, column_property, Mapped, mapped_column
from sqlalchemy import (
    Numeric,
    String,
    Enum,
    Integer,
    Text,
    Boolean,
    UUID,
    select,
    and_,
    or_,
    ForeignKey,
)

# models
from app.modules.contract.models.under_contract import UnderContract
from app.modules.properties.models.property_unit_association import PropertyUnitAssoc

# enums
from app.modules.properties.enums.property_enums import PropertyStatus

from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


# TODO: (DQ) Review calendar events
# - review if this is needed is_contract_active
class Units(PropertyUnitAssoc):
    __tablename__ = "units"

    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
        primary_key=True,
    )
    property_unit_code: Mapped[str] = mapped_column(String(128))
    property_unit_floor_space: Mapped[int] = mapped_column(Integer)
    property_unit_amount: Mapped[float] = mapped_column(Numeric(10, 2))
    property_unit_security_deposit: Mapped[float] = mapped_column(Numeric(10, 2))
    property_unit_commission: Mapped[float] = mapped_column(Numeric(10, 2))
    property_floor_id: Mapped[int] = mapped_column(Integer)
    property_status: Mapped[PropertyStatus] = mapped_column(Enum(PropertyStatus))
    property_unit_notes: Mapped[str] = mapped_column(Text)
    has_amenities: Mapped[bool] = mapped_column(Boolean, default=False)
    property_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("property.property_unit_assoc_id")
    )

    __mapper_args__ = {
        "polymorphic_identity": "Units",
        "inherit_condition": property_unit_assoc_id
        == PropertyUnitAssoc.property_unit_assoc_id,
    }

    is_contract_active: Mapped[bool] = column_property(
        select(UnderContract.contract_number)
        .where(
            and_(
                UnderContract.property_unit_assoc_id == property_unit_assoc_id,
                UnderContract.start_date <= datetime.now(),
                or_(
                    UnderContract.end_date.is_(None),
                    UnderContract.end_date >= datetime.now(),
                ),
            )
        )
        .exists()
    )

    # maintenance_requests
    maintenance_requests: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest",
        primaryjoin="Units.property_unit_assoc_id == MaintenanceRequest.property_unit_assoc_id",
        foreign_keys="[MaintenanceRequest.property_unit_assoc_id]",
        lazy="selectin",
        back_populates="unit",
        viewonly=True,
    )

    # tour_bookings
    tour_bookings: Mapped[List["Tour"]] = relationship(
        "Tour",
        primaryjoin="Units.property_unit_assoc_id == Tour.property_unit_assoc_id",
        foreign_keys="[Tour.property_unit_assoc_id]",
        lazy="selectin",
        back_populates="unit",
        viewonly=True,
    )

    # utilities
    utilities: Mapped[List["EntityBillable"]] = relationship(
        "EntityBillable",
        primaryjoin="and_(EntityBillable.entity_id==Units.property_unit_assoc_id,  EntityBillable.entity_type=='units', EntityBillable.billable_type=='utilities')",
        foreign_keys="[EntityBillable.entity_id]",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # property
    property: Mapped["Property"] = relationship(
        "Property",
        primaryjoin="Units.property_id == Property.property_unit_assoc_id",
        back_populates="units",
        cascade="all, delete",
        lazy="selectin",
    )

    property_unit_assoc = relationship("PropertyUnitAssoc", back_populates="units")

    # media
    media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary="entity_media",
        primaryjoin="and_(EntityMedia.entity_id==Units.property_unit_assoc_id, EntityMedia.entity_type=='units')",
        secondaryjoin="EntityMedia.media_id == Media.media_id",
        # overlaps="entity_media,media",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # entity_amenities
    entity_amenities: Mapped[List["EntityAmenities"]] = relationship(
        "EntityAmenities",
        primaryjoin="Units.property_unit_assoc_id == EntityAmenities.entity_id",
        foreign_keys="[EntityAmenities.entity_id]",
        lazy="selectin",
        viewonly=True,
    )

    # amenities
    amenities: Mapped[List["Amenities"]] = relationship(
        "Amenities",
        secondary="entity_amenities",
        primaryjoin="Units.property_unit_assoc_id == EntityAmenities.entity_id",
        secondaryjoin="EntityAmenities.amenity_id == Amenities.amenity_id",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # property_assignment
    assigned_users: Mapped[List["PropertyAssignment"]] = relationship(
        "PropertyAssignment", lazy="selectin", viewonly=True
    )


# Register model outside the class definition
Base.setup_model_dynamic_listener("units", Units)
