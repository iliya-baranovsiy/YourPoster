from typing import Callable, Dict, Any, Awaitable
from dataclasses import dataclass
from aiogram.types import CallbackQuery
from aiogram import BaseMiddleware
from redisWork.autopostingCash.user_payment_cash import user_payment_cash
from redisWork.autopostingCash.cash_validator import cash_validator


@dataclass
class SubscribeCash:
    payment_plan: str
    end_date: str
    balance: float
    auto_pay: bool

    def __post_init__(self):
        self.balance = round(self.balance, 2)


class SubscribeInfoMiddleware(BaseMiddleware):

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        tg_id = event.from_user.id
        is_cashing = False
        update = False
        subscribe_info = None
        cash = await user_payment_cash.get_cash(tg_id)
        if cash:
            is_cashing = True
            subscribe_info = SubscribeCash(
                payment_plan=cash['payment_plan'],
                end_date=cash['end_date'],
                balance=cash['balance'],
                auto_pay=cash['auto_pay']
            )
        else:
            update = await cash_validator.inc_check_callback_count(tg_id=tg_id)
        data.update(subscribe_info=subscribe_info, cashing=is_cashing, update=update)

        return await handler(event, data)
