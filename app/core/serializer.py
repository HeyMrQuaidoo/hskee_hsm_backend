from fastapi.encoders import jsonable_encoder
from typing import Any, Type, Optional
import json

class JSONSerializer:
    """
    Utility class for serializing and deserializing data to/from JSON, handling special types.
    """

    @staticmethod
    def serialize(obj: Any) -> str:
        """
        Serialize data into a JSON string, handling special types.
        """
        try:
            json_compatible_data = jsonable_encoder(obj)
            return json.dumps(json_compatible_data)
        except Exception as e:
            raise e

    @staticmethod
    def deserialize(
        data: str,
        model_class: Optional[Type[Any]] = None
    ) -> Any:
        """
        Deserialize a JSON string back into data, optionally into a Pydantic model instance.
        """
        if data is None:
            return None

        obj = json.loads(data)

        if model_class and hasattr(model_class, 'parse_obj'):
            return model_class.parse_obj(obj)
        return obj
