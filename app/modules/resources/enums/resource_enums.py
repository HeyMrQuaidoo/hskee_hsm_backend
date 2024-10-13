import enum


class AmenityValueType(enum.Enum):
    boolean = "boolean"
    number = "number"


class MediaType(enum.Enum):
    image = "image"
    video = "video"
    audio = "audio"
    document = "document"
    other = "other"
