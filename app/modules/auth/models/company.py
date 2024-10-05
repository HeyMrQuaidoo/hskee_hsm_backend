import uuid
from typing import List
from sqlalchemy import String, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

# models
from app.modules.common.models.model_base import BaseModel as Base


class Company(Base):
    __tablename__ = "company"

    company_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True)
    company_name: Mapped[str] = mapped_column(String(80))
    company_website: Mapped[str] = mapped_column(String(80))

    # users
    users: Mapped[List["User"]] = relationship(
        "User",
        secondary="entity_company",
        secondaryjoin="and_(Company.company_id==EntityCompany.company_id, EntityCompany.entity_type=='Users')",
        primaryjoin="and_(User.user_id==EntityCompany.entity_id)",
        back_populates="company",
    )
