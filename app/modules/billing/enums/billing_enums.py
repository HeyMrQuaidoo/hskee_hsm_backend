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


class PaymentTypeEnum(enum.Enum):
    annually = "Annually"
    monthly = "Monthly"
    weekly = "Weekly"
    one_time = "One-time"
    quarterly = "Quarterly"
    bi_annual = "Bi-Annual"
    custom = "Custom"


class TransactionTypeEnum(enum.Enum):
    card = "Card"
    mobile_money = "Mobile Money"
    visa = "Visa"
    paypal = "PayPal"
    refund = "Refund"
    credit = "Credit"
    debit = "Debit"
    bank_transfer = "Bank Transfer"
    cash = "Cash"
    cryptocurrency = "Cryptocurrency"
    check = "Check"
    direct_debit = "Direct Debit"
    ewallet = "E-Wallet"
    prepaid_card = "Prepaid Card"
    net_banking = "Net Banking"
    wire_transfer = "Wire Transfer"
    pos = "Point of Sale (POS)"
    google_pay = "Google Pay"
    apple_pay = "Apple Pay"
    stripe = "Stripe"
    square = "Square"
