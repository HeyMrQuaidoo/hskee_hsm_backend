from pydantic import BaseModel, UUID4

# Base Faker for generating example data
from app.modules.common.schema.base_schema import BaseFaker

# Models
from app.modules.auth.models.favorite_properties import (
    FavoriteProperties as FavoritePropertiesModel,
)


class FavoritePropertiesBase(BaseModel):
    user_id: UUID4
    property_unit_assoc_id: UUID4

    class Config:
        from_attributes = True


class FavoriteProperties(FavoritePropertiesBase):
    favorite_id: UUID4


class FavoritePropertiesInfoMixin:
    _user_id = BaseFaker.uuid4()
    _property_unit_assoc_id = BaseFaker.uuid4()

    _favorite_properties_create_json = {
        "user_id": _user_id,
        "property_unit_assoc_id": _property_unit_assoc_id,
    }

    _favorite_properties_update_json = {
        "user_id": _user_id,
        "property_unit_assoc_id": _property_unit_assoc_id,
    }

    @classmethod
    def get_favorite_properties_info(
        cls, favorite: FavoritePropertiesModel
    ) -> FavoriteProperties:
        return FavoriteProperties(
            favorite_id=favorite.favorite_id,
            user_id=favorite.user_id,
            property_unit_assoc_id=favorite.property_unit_assoc_id,
        )

    @classmethod
    def model_validate(cls, favorite: FavoritePropertiesModel):
        return cls(
            favorite_id=favorite.favorite_id,
            user_id=favorite.user_id,
            property_unit_assoc_id=favorite.property_unit_assoc_id,
        )
