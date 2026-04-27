from decimal import Decimal
from datetime import date
from typing import Optional

from pydantic import BaseModel


class BaseParameters(BaseModel):
    channels: list[tuple]
    payment_plan: str
