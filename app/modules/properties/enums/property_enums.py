import enum


class PropertyAssignmentType(enum.Enum):
    other = "other"
    handler = "handler"
    landlord = "landlord"
    contractor = "contractor"


class PropertyStatus(enum.Enum):
    sold = "sold"
    rent = "rent"
    lease = "lease"
    bought = "bought"
    available = "available"
    unavailable = "unavailable"


class PropertyType(enum.Enum):
    residential = "residential"
    commercial = "commercial"
    industrial = "industrial"
