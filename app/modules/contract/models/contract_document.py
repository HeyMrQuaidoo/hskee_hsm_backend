import uuid
from sqlalchemy import ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column
from app.modules.common.models.model_base import BaseModel as Base


class ContractDocument(Base):
    __tablename__ = "contract_document"

    contract_document_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        unique=True,
        index=True,
        default=uuid.uuid4,
    )
    contract_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("contract.contract_id")
    )
    document_number: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("document.document_number")
    )
