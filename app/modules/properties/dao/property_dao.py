from typing import List, Optional
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

# Models
from app.modules.properties.models.property import Property
from app.modules.resources.models.amenity import Amenities
from app.modules.properties.models.unit import Units
from app.modules.resources.models.media import Media
from app.modules.billing.models.utility import Utilities
from app.modules.associations.models.entity_amenities import EntityAmenities
from app.modules.associations.models.entity_media import EntityMedia
from app.modules.associations.models.entity_billable import EntityBillable

# Enums
from app.modules.associations.enums.entity_type_enums import EntityTypeEnum
from app.modules.resources.enums.resource_enums import MediaType
from app.modules.billing.enums.billing_enums import BillableTypeEnum

# DAO
from app.modules.common.dao.base_dao import BaseDAO
from app.modules.address.dao.address_dao import AddressDAO

# Core
from app.core.response import DAOResponse
from app.core.errors import RecordNotFoundException


class PropertyDAO(BaseDAO[Property]):
    def __init__(self, excludes: Optional[List[str]] = None):
        self.model = Property
        self.address_dao = AddressDAO()
        self.unit_dao = BaseDAO(
            model=Units,
            detail_mappings={"address": self.address_dao},
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )
        self.detail_mappings = {
            "address": self.address_dao,
            "units": self.unit_dao
        }
        super().__init__(
            model=self.model,
            detail_mappings=self.detail_mappings,
            excludes=excludes,
            primary_key="property_unit_assoc_id",
        )


    async def add_amenities(
        self,
        db_session: AsyncSession,
        property_id: UUID,
        amenity_ids: List[UUID],
        apply_to_units: bool = False,
    ) -> DAOResponse:
        try:
            # Check if property exists
            property = await self.get(db_session=db_session, id=property_id)
            if not property:
                raise RecordNotFoundException(model="Property", id=property_id)

            for amenity_id in amenity_ids:
                # Check if amenity exists
                result = await db_session.execute(
                    select(Amenities).where(Amenities.amenity_id == amenity_id)
                )
                amenity = result.scalar_one_or_none()
                if not amenity:
                    raise RecordNotFoundException(model="Amenity", id=amenity_id)

                # Create EntityAmenities association
                entity_amenity = EntityAmenities(
                    amenity_id=amenity_id,
                    entity_id=property_id,
                    entity_type=EntityTypeEnum.property,
                    apply_to_units=apply_to_units,
                )
                db_session.add(entity_amenity)

            await db_session.commit()
            return DAOResponse(
                success=True, data={"message": "Amenities added to property"}
            )
        except Exception as e:
            await db_session.rollback()
            raise e

    async def get_amenities(
        self, db_session: AsyncSession, property_id: UUID
    ) -> List[Amenities]:
        try:
            result = await db_session.execute(
                select(Amenities)
                .join(
                    EntityAmenities,
                    Amenities.amenity_id == EntityAmenities.amenity_id,
                )
                .where(
                    EntityAmenities.entity_id == property_id,
                    EntityAmenities.entity_type == EntityTypeEnum.property,
                )
            )
            amenities = result.scalars().all()
            return amenities
        except Exception as e:
            raise e

    async def remove_amenity(
        self, db_session: AsyncSession, property_id: UUID, amenity_id: UUID
    ) -> None:
        try:
            result = await db_session.execute(
                select(EntityAmenities).where(
                    EntityAmenities.entity_id == property_id,
                    EntityAmenities.entity_type == EntityTypeEnum.property,
                    EntityAmenities.amenity_id == amenity_id,
                )
            )
            entity_amenity = result.scalar_one_or_none()
            if not entity_amenity:
                raise RecordNotFoundException(
                    model="EntityAmenities",
                    id=f"property_id={property_id}, amenity_id={amenity_id}",
                )
            await db_session.delete(entity_amenity)
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e

    async def add_media(
        self, db_session: AsyncSession, property_id: UUID, media_list: List[dict]
    ) -> DAOResponse:
        try:
            # Check if property exists
            property = await self.get(db_session=db_session, id=property_id)
            if not property:
                raise RecordNotFoundException(model="Property", id=property_id)

            for media_data in media_list:
                # Create Media entry
                media = Media(**media_data)
                db_session.add(media)
                await db_session.flush()  # To get media_id

                # Create EntityMedia association
                entity_media = EntityMedia(
                    media_id=media.media_id,
                    entity_id=property_id,
                    entity_type=EntityTypeEnum.property,
                    media_type=media.media_type,
                )
                db_session.add(entity_media)

            await db_session.commit()
            return DAOResponse(
                success=True,
                data={"message": "Media uploaded and associated with property"},
            )
        except Exception as e:
            await db_session.rollback()
            raise e

    async def get_media(
        self, db_session: AsyncSession, property_id: UUID
    ) -> List[Media]:
        try:
            result = await db_session.execute(
                select(Media)
                .join(EntityMedia, Media.media_id == EntityMedia.media_id)
                .where(
                    EntityMedia.entity_id == property_id,
                    EntityMedia.entity_type == EntityTypeEnum.property,
                )
            )
            media_items = result.scalars().all()
            return media_items
        except Exception as e:
            raise e

    async def remove_media(
        self, db_session: AsyncSession, property_id: UUID, media_id: UUID
    ) -> None:
        try:
            result = await db_session.execute(
                select(EntityMedia).where(
                    EntityMedia.entity_id == property_id,
                    EntityMedia.entity_type == EntityTypeEnum.property,
                    EntityMedia.media_id == media_id,
                )
            )
            entity_media = result.scalar_one_or_none()
            if not entity_media:
                raise RecordNotFoundException(
                    model="EntityMedia",
                    id=f"property_id={property_id}, media_id={media_id}",
                )
            await db_session.delete(entity_media)
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e

    async def add_utilities(
        self, db_session: AsyncSession, property_id: UUID, utilities: List[dict]
    ) -> DAOResponse:
        try:
            # Check if property exists
            property = await self.get(db_session=db_session, id=property_id)
            if not property:
                raise RecordNotFoundException(model="Property", id=property_id)

            for utility_data in utilities:
                utility_id = utility_data.get("billable_assoc_id")
                billable_amount = utility_data.get("billable_amount", 0.0)
                apply_to_units = utility_data.get("apply_to_units", False)

                # Check if utility exists
                result = await db_session.execute(
                    select(Utilities).where(
                        Utilities.billable_assoc_id == utility_id
                    )
                )
                utility = result.scalar_one_or_none()
                if not utility:
                    raise RecordNotFoundException(model="Utility", id=utility_id)

                # Create EntityBillable association
                entity_billable = EntityBillable(
                    entity_id=property_id,
                    entity_type=EntityTypeEnum.property,
                    billable_id=utility_id,
                    billable_type=BillableTypeEnum.utilities,
                    billable_amount=billable_amount,
                    apply_to_units=apply_to_units,
                )
                db_session.add(entity_billable)

            await db_session.commit()
            return DAOResponse(
                success=True, data={"message": "Utilities added to property"}
            )
        except Exception as e:
            await db_session.rollback()
            raise e

    async def get_utilities(
        self, db_session: AsyncSession, property_id: UUID
    ) -> List[Utilities]:
        try:
            result = await db_session.execute(
                select(Utilities)
                .join(
                    EntityBillable,
                    Utilities.billable_assoc_id == EntityBillable.billable_id,
                )
                .where(
                    EntityBillable.entity_id == property_id,
                    EntityBillable.entity_type == EntityTypeEnum.property,
                    EntityBillable.billable_type == BillableTypeEnum.utilities,
                )
            )
            utilities = result.scalars().all()
            return utilities
        except Exception as e:
            raise e

    async def remove_utility(
        self, db_session: AsyncSession, property_id: UUID, utility_id: UUID
    ) -> None:
        try:
            result = await db_session.execute(
                select(EntityBillable).where(
                    EntityBillable.entity_id == property_id,
                    EntityBillable.entity_type == EntityTypeEnum.property,
                    EntityBillable.billable_id == utility_id,
                    EntityBillable.billable_type == BillableTypeEnum.utilities,
                )
            )
            entity_billable = result.scalar_one_or_none()
            if not entity_billable:
                raise RecordNotFoundException(
                    model="EntityBillable",
                    id=f"property_id={property_id}, utility_id={utility_id}",
                )
            await db_session.delete(entity_billable)
            await db_session.commit()
        except Exception as e:
            await db_session.rollback()
            raise e


    async def get_utility_billable_details(
            self, db_session: AsyncSession, property_id: UUID, utility_id: UUID
        ) -> EntityBillable:
            try:
                result = await db_session.execute(
                    select(EntityBillable)
                    .where(
                        EntityBillable.entity_id == property_id,
                        EntityBillable.entity_type == EntityTypeEnum.property,
                        EntityBillable.billable_id == utility_id,
                        EntityBillable.billable_type == BillableTypeEnum.utilities,
                    )
                )
                entity_billable = result.scalar_one_or_none()
                if not entity_billable:
                    raise RecordNotFoundException(
                        model="EntityBillable",
                        id=f"property_id={property_id}, utility_id={utility_id}",
                    )
                return entity_billable
            except Exception as e:
                raise e

    async def update_utility_billable_details(
            self,
            db_session: AsyncSession,
            property_id: UUID,
            utility_id: UUID,
            billable_update: dict,
        ) -> EntityBillable:
            try:
                entity_billable = await self.get_utility_billable_details(
                    db_session=db_session,
                    property_id=property_id,
                    utility_id=utility_id,
                )
                for key, value in billable_update.items():
                    setattr(entity_billable, key, value)
                await db_session.commit()
                await db_session.refresh(entity_billable)
                return entity_billable
            except Exception as e:
                await db_session.rollback()
                raise e