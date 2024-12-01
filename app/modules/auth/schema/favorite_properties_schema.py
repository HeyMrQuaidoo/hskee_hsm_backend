from pydantic import UUID4, ConfigDict
from typing import Optional


# Models
from app.modules.auth.models.favorite_properties import FavoriteProperties as FavoritePropertiesModel

# Mixins
from app.modules.auth.schema.mixins.favorite_properties_mixin import FavoritePropertiesBase, FavoritePropertiesInfoMixin



class FavoritePropertiesCreateSchema(FavoritePropertiesBase, FavoritePropertiesInfoMixin):
    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={"example": FavoritePropertiesInfoMixin._favorite_properties_create_json},
    )

    @classmethod
    def model_validate(cls, favorite: FavoritePropertiesModel):
        return cls.get_favorite_properties_info(favorite)


class FavoritePropertiesUpdateSchema(FavoritePropertiesBase, FavoritePropertiesInfoMixin):
    user_id: Optional[UUID4] = None
    property_unit_assoc_id: Optional[UUID4] = None

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed=True,
        json_schema_extra={"example": FavoritePropertiesInfoMixin._favorite_properties_update_json},
    )

    @classmethod
    def model_validate(cls, favorite: FavoritePropertiesModel):
        """
        Validates and maps a FavoritePropertiesModel instance to the Update schema.
        """
        return cls(**cls.get_favorite_properties_info(favorite))
    


class FavoritePropertiesResponse(FavoritePropertiesModel, FavoritePropertiesInfoMixin):
    @classmethod
    def model_validate(cls, favorite: FavoritePropertiesModel):
        return cls.get_favorite_properties_info(favorite)
