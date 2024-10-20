import enum


class ContractStatusEnum(enum.Enum):
    active = "active"
    inactive = "inactive"
    expired = "expired"
    pending = "pending"
    terminated = "terminated"


class ContractTypeEnum(enum.Enum):
    annual = "Annual"
    monthly = "Monthly"
    weekly = "Weekly"
    one_time = "One-time"
