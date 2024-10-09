import uuid
from sqlalchemy import String, UUID, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

# models
from app.modules.common.models.model_base import BaseModel as Base


class Document(Base):
    __tablename__ = "document"

    document_number: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True
    )
    name: Mapped[str] = mapped_column(String(128))
    content_url: Mapped[str] = mapped_column(String(128))
    content_type: Mapped[str] = mapped_column(String(128))
    uploaded_by: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.user_id")
    )

    # users
    users: Mapped["User"] = relationship("User", back_populates="documents")

    # contracts
    contract: Mapped[list["Contract"]] = relationship(
        "Contract", secondary="contract_document", back_populates="contract_documents"
    )
