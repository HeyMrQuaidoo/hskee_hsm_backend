import enum


class ContractStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"
    pending = "pending"
    terminated = "terminated"
