from decimal import Decimal
from datetime import date
from typing import Optional

from pydantic import BaseModel


class PaymentDTO(BaseModel):
    balance: Decimal
    payment_plan: str
    end_date: Optional[date]

    @property
    def get_end_day(self):
        if self.end_date != None:
            return self.end_date.strftime('%d-%m-%Y')
        else:
            return "Безлимитно"
