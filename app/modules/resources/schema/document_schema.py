from pydantic import UUID4
from app.modules.common.schema.base_schema import BaseSchema


class DocumentBase(BaseSchema):
    name: str
    content_url: str
    content_type: str
    uploaded_by: UUID4


class Document(BaseSchema):
    document_number: UUID4
