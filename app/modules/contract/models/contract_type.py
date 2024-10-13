from sqlalchemy import Numeric, String, Integer
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class ContractType(Base):
    __tablename__ = "contract_type"

    contract_type_id: Mapped[int] = mapped_column(
        Integer, primary_key=True, unique=True, index=True, autoincrement=True
    )
    contract_type_name: Mapped[str] = mapped_column(String(128))
    fee_percentage: Mapped[float] = mapped_column(Numeric(5, 2))

    # contracts
    contracts: Mapped[list["Contract"]] = relationship(
        "Contract", back_populates="contract_type"
    )
