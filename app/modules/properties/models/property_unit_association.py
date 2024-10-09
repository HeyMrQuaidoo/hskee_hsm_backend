import uuid
from typing import List
from sqlalchemy import String, UUID
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class PropertyUnitAssoc(Base):
    __tablename__ = "property_unit_assoc"

    property_unit_assoc_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    property_unit_type: Mapped[str] = mapped_column(String)

    __mapper_args__ = {
        "polymorphic_on": property_unit_type,
        "polymorphic_identity": "property_unit_assoc",
    }

    # units
    units: Mapped[List["Property"]] = relationship(
        "Property",
        primaryjoin="and_(PropertyUnitAssoc.property_unit_type == 'Property', Property.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id)",
        foreign_keys="[Property.property_unit_assoc_id]",
        remote_side="[PropertyUnitAssoc.property_unit_assoc_id]",
        lazy="selectin",
        viewonly=True,
    )

    # property
    property: Mapped[List["Units"]] = relationship(
        "Units",
        primaryjoin="and_(PropertyUnitAssoc.property_unit_type == 'Units', Units.property_unit_assoc_id == PropertyUnitAssoc.property_unit_assoc_id)",
        foreign_keys="[Units.property_unit_assoc_id]",
        remote_side="[PropertyUnitAssoc.property_unit_assoc_id]",
        lazy="selectin",
        viewonly=True,
    )

    # members
    members: Mapped[List["User"]] = relationship(
        "User",
        secondary="under_contract",
        primaryjoin="and_(PropertyUnitAssoc.property_unit_assoc_id == UnderContract.property_unit_assoc_id)",
        secondaryjoin="and_(UnderContract.client_id == User.user_id)",
        foreign_keys="[UnderContract.property_unit_assoc_id, UnderContract.client_id]",
        overlaps="client_representative, properties",
    )

    # utilities
    utilities: Mapped[List["Utilities"]] = relationship(
        "Utilities",
        secondary="entity_billable",
        primaryjoin="and_(EntityBillable.entity_id==PropertyUnitAssoc.property_unit_assoc_id,  EntityBillable.entity_type=='Property',  EntityBillable.billable_type=='Utilities')",
        secondaryjoin="and_(EntityBillable.billable_id == Utilities.utility_id)",
        foreign_keys="[EntityBillable.entity_id, Utilities.utility_id]",
        lazy="selectin",
        viewonly=True,
        # overlaps="entity_billable,utilities",
    )

    # property_assignments
    assignments: Mapped[List["User"]] = relationship(
        "User", secondary="property_assignment", back_populates="property_assignments"
    )

    # amenities
    amenities: Mapped[List["Amenities"]] = relationship(
        "Amenities",
        secondary="entity_amenities",
        primaryjoin="and_(EntityAmenities.entity_id==PropertyUnitAssoc.property_unit_assoc_id)",
        overlaps="amenities",
    )

    # message recipients
    messages_recipients: Mapped[List["MessageRecipient"]] = relationship(
        "MessageRecipient", back_populates="message_group", lazy="selectin"
    )

    # contracts
    under_contract: Mapped[List["UnderContract"]] = relationship(
        "UnderContract",
        back_populates="properties",
        # overlaps="members",
        lazy="selectin",
        viewonly=True,
    )

    # maintenance_requests
    prop_maintenance_requests: Mapped[List["MaintenanceRequest"]] = relationship(
        "MaintenanceRequest",
        back_populates="property_unit_assoc",
        cascade="save-update, merge",
        foreign_keys="[MaintenanceRequest.property_unit_assoc_id]",
    )

    # tours
    prop_unit_assoc_tours: Mapped[List["Tour"]] = relationship(
        "Tour",
        back_populates="property_unit_assoc",
        cascade="save-update, merge",
        foreign_keys="[Tour.property_unit_assoc_id]",
    )
