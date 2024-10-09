from app.core.response_mapping import response_mapping
from typing import Any, Dict, Type, TypeVar, Generic, Optional
from pydantic import BaseModel, ConfigDict, ValidationError, model_serializer

T = TypeVar("T")


class DAOResponse(BaseModel, Generic[T]):
    success: bool = False
    error: Optional[str] = None
    data: Optional[T | Any] = None
    meta: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

    def __init__(
        self,
        *,
        success: bool,
        data: Optional[T] = None,
        error: Optional[str] = None,
        validation_error: Optional[ValidationError] = None,
        meta: Optional[Dict[str, Any]] = None,
        **kwargs,
    ):
        super().__init__(success=success, data=data, error=error, **kwargs)

        self.data = self._convert_data(data)
        self.error = "" if error is None else error
        self.meta = meta

        if validation_error:
            self.set_validation_errors(validation_error)

    def _convert_data(self, data: Any) -> Any:
        """Convert the data to the appropriate response object based on its type."""
        if not data:
            return data

        response_class = response_mapping.get(
            type(data[0]) if isinstance(data, list) else type(data)
        )

        print(f"response_class {response_class} {type(response_class)}")
        if not response_class:
            return data

        return (
            [response_class.model_validate(item) for item in data]
            if isinstance(data, list)
            else response_class.model_validate(data)
        )

    def set_validation_errors(self, validation_error: ValidationError):
        error_messages = []
        for error in validation_error.errors():
            field = error["loc"][0]
            message = error["msg"]
            error_messages.append(f"{field} validation is incorrect: {message}")
        self.error = "; ".join(error_messages)

    def set_meta(self, meta):
        self.meta = meta

    @model_serializer(when_used="json")
    def dump_model(self) -> Dict[str, Any]:
        result = super().model_dump()

        if not self.meta:
            result.pop("meta", None)
        elif hasattr(self.meta, "total") and getattr(self.meta, "total") == 0:
            result.pop("meta", None)

        return result

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "error": self.error,
            "data": self.data if self.data else None,
            "meta": self.meta if self.meta else None,
        }

    @classmethod
    def from_orm(cls: Type[T], obj: Any) -> T:
        return cls.model_validate(obj)

    @classmethod
    def model_validate(cls: Type[T], obj: Any) -> T:
        return cls.model_validate(obj)
