import enum


class EntityTypeEnum(enum.Enum):
    property = "property"
    units = "units"
    utilities = "utilities"
    contract = "contract"
    user = "user"
    role = "role"
    amenities = "amenities"
    account = "account"
    comapany = "comapany"
    entityamenities = "entityamenities"
    pastrentalhistory = "pastrentalhistory"
    # maintenancerequests = "maintenancerequests"
    maintenance_requests = "maintenance_requests"
