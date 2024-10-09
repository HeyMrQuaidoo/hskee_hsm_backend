from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class PropertyType(Base):
    __tablename__ = "property_type"

    property_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)
