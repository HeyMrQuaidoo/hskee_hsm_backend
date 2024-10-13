from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

# modesl
from app.modules.common.models.model_base import BaseModel as Base


class UnitType(Base):
    __tablename__ = "unit_type"

    unit_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, index=True, autoincrement=True
    )
    unit_type_name: Mapped[str] = mapped_column(String(128))
