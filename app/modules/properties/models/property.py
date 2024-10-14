from datetime import datetime
from typing import List, Optional
import uuid
from sqlalchemy.orm import relationship, column_property, Mapped, mapped_column
from sqlalchemy import (
    Numeric,
    String,
    Enum,
    Integer,
    Text,
    Boolean,
    UUID,
    ForeignKey,
    select,
    and_,
    or_,
)


# models
from app.modules.contract.models.under_contract import UnderContract
from app.modules.properties.models.property_unit_association import PropertyUnitAssoc

# enums
from app.modules.properties.enums.property_enums import PropertyStatus, PropertyType

from app.modules.common.models.model_base import BaseModel as Base, BaseModelCollection


# TODO: (DQ) Review calendar events
# - review if this is needed is_contract_active

class Property(PropertyUnitAssoc):
    __tablename__ = "property"

    # Fields
    name: Mapped[str] = mapped_column(String(255))
    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("property_unit_assoc.property_unit_assoc_id", ondelete="CASCADE"),
        primary_key=True,
    )
    property_type: Mapped[PropertyType] = mapped_column(Enum(PropertyType))
    amount: Mapped[float] = mapped_column(Numeric(10, 2))
    security_deposit: Mapped[float] = mapped_column(Numeric(10, 2))
    commission: Mapped[float] = mapped_column(Numeric(10, 2))
    floor_space: Mapped[float] = mapped_column(Numeric(8, 2))
    num_units: Mapped[int] = mapped_column(Integer)
    num_bathrooms: Mapped[int] = mapped_column(Integer)
    num_garages: Mapped[int] = mapped_column(Integer)
    has_balconies: Mapped[bool] = mapped_column(Boolean, default=False)
    has_parking_space: Mapped[bool] = mapped_column(Boolean, default=False)
    pets_allowed: Mapped[bool] = mapped_column(Boolean, default=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    property_status: Mapped[PropertyStatus] = mapped_column(Enum(PropertyStatus))

    __mapper_args__ = {
        "polymorphic_identity": "Property",
        "inherit_condition": property_unit_assoc_id
        == PropertyUnitAssoc.property_unit_assoc_id,
    }

    # Computed Property
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

    # Relationships

    # Maintenance Requests
    maintenance_requests: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest",
        primaryjoin="Property.property_unit_assoc_id == MaintenanceRequest.property_unit_assoc_id",
        foreign_keys="[MaintenanceRequest.property_unit_assoc_id]",
        lazy="selectin",
        back_populates="property",
        viewonly=True,
    )

    # Tour Bookings
    tour_bookings: Mapped[List["Tour"]] = relationship(
        "Tour",
        primaryjoin="Property.property_unit_assoc_id == Tour.property_unit_assoc_id",
        foreign_keys="[Tour.property_unit_assoc_id]",
        lazy="selectin",
        back_populates="property",
        viewonly=True,
    )

    # Units
    units: Mapped[List["Units"]] = relationship(
        "Units",
        primaryjoin="Property.property_unit_assoc_id == Units.property_id",
        back_populates="property",
        lazy="selectin",
        collection_class=BaseModelCollection,
        viewonly=True,
    )

    # Entity Media Relationship
    entity_media: Mapped[List["EntityMedia"]] = relationship(
        "EntityMedia",
        primaryjoin="and_(foreign(Property.property_unit_assoc_id) == EntityMedia.entity_id, EntityMedia.entity_type == 'property')",
        lazy="selectin",
    )

    # Media
    media: Mapped[List["Media"]] = relationship(
        "Media",
        secondary="entity_media",
        primaryjoin="and_(Property.property_unit_assoc_id == EntityMedia.entity_id, EntityMedia.entity_type == 'property')",
        secondaryjoin="EntityMedia.media_id == Media.media_id",
        viewonly=True,
        lazy="selectin",
        collection_class=BaseModelCollection,
    )

    # Entity Amenities
    entity_amenities: Mapped[List["EntityAmenities"]] = relationship(
        "EntityAmenities",
        primaryjoin="Property.property_unit_assoc_id == EntityAmenities.entity_id",
        foreign_keys="[EntityAmenities.entity_id]",
        lazy="selectin",
        viewonly=True,
        cascade="all, delete-orphan",
    )

    # Amenities
    amenities: Mapped[List["Amenities"]] = relationship(
        "Amenities",
        secondary="entity_amenities",
        primaryjoin="Property.property_unit_assoc_id == EntityAmenities.entity_id",
        secondaryjoin="EntityAmenities.amenity_id == Amenities.amenity_id",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # Utilities
    utilities: Mapped[List["Utilities"]] = relationship(
        "Utilities",
        secondary="entity_billable",
        primaryjoin="and_(Property.property_unit_assoc_id == EntityBillable.entity_id, EntityBillable.entity_type == 'property', EntityBillable.billable_type=='utilities')",
        secondaryjoin="EntityBillable.billable_id == Utilities.billable_assoc_id",
        back_populates="properties",
        overlaps="entity_billables",
        lazy="selectin",
        collection_class=BaseModelCollection,
    )

    # Addresses
    address: Mapped[List["Addresses"]] = relationship(
        "Addresses",
        secondary="entity_address",
        primaryjoin="and_(Property.property_unit_assoc_id == EntityAddress.entity_id, EntityAddress.entity_type == 'property')",
        secondaryjoin="EntityAddress.address_id == Addresses.address_id",
        back_populates="properties",
        lazy="selectin",
        viewonly=True,
        collection_class=BaseModelCollection,
    )

    # Assigned Users
    assigned_users: Mapped[List["PropertyAssignment"]] = relationship(
        "PropertyAssignment", lazy="selectin", viewonly=True
    )

    # calendar event
    # events = relationship(
    #     "CalendarEvent",
    #     secondary="property_unit_assoc",
    #     primaryjoin="CalendarEvent.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id",
    #     back_populates="property",
    # )


# Register model outside the class definition
Base.setup_model_dynamic_listener("property", Property)
