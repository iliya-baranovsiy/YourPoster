from decimal import Decimal
from datetime import date
from typing import Optional

from pydantic import BaseModel


class PaymentDTO(BaseModel):
    balance: Decimal
    payment_plan: str
    end_date_row: Optional[date]
    auto_pay: bool

    @property
    def end_date(self):
        if self.end_date_row != None:
            return self.end_date_row.strftime('%d-%m-%Y')
        else:
            return "Безлимитно"
