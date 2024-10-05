import enum


class AmenityValueType(enum.Enum):
    boolean = "boolean"
    number = "number"


class MediaType(enum.Enum):
    document = "document"
    image = "image"
    video = "video"
    other = "other"
