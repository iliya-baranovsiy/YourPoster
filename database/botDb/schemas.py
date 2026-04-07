from decimal import Decimal
from datetime import date
from typing import Optional

from pydantic import BaseModel


class PaymentDTO(BaseModel):
    balance: Decimal
    payment_plan: str
    activate_date: Optional[date]
    end_date: Optional[date]
