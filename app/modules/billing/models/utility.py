import uuid
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, UUID, Text, ForeignKey

# models
from app.modules.billing.models.billable import BillableAssoc


class Utilities(BillableAssoc):
    __tablename__ = "utilities"

    utility_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("billable_assoc.billable_assoc_id"),
        primary_key=True,
    )
    name: Mapped[str] = mapped_column(String(128))
    description: Mapped[str] = mapped_column(Text)

    __mapper_args__ = {
        "polymorphic_identity": "Utilities",
        "inherit_condition": utility_id == BillableAssoc.billable_assoc_id,
    }
