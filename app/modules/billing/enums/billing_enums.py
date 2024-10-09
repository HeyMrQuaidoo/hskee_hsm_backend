import enum


class AccountTypeEnum(enum.Enum):
    savings = "savings"
    billing = "billing"
    debit = "debit"
    credit = "credit"
    general = "general"


class CompanyTypeEnum(enum.Enum):
    agency = "agency"
    sole_proprietor = "sole_proprietor"


class BillableTypeEnum(enum.Enum):
    utilities = "utilities"
    maintenance_requests = "maintenance_requests"


class PaymentStatusEnum(enum.Enum):
    pending = "pending"
    completed = "completed"
    cancelled = "cancelled"
    reversal = "reversal"


class InvoiceTypeEnum(enum.Enum):
    lease = "lease"
    maintenance = "maintenance"
    other = "other"
    general = "general"
