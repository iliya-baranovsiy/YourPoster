import enum


class PaymentOptions(str, enum.Enum):
    STANDART = "STANDART",
    PRO = "PRO",
    VIP = "VIP"
