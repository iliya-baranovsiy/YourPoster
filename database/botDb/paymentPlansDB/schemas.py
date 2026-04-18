from decimal import Decimal
from datetime import date
from typing import Optional

from pydantic import BaseModel


class PaymentDTO(BaseModel):
    balance: Decimal | None
    payment_plan: str | None
    end_date_row: Optional[date] | None
    auto_pay: bool | None

    @property
    def end_date(self):
        if self.end_date_row != None:
            return self.end_date_row.strftime('%d-%m-%Y')
        else:
            return "Безлимитно"
