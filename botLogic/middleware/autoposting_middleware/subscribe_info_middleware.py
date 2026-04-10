from typing import Callable, Dict, Any, Awaitable
from dataclasses import dataclass
from aiogram.types import CallbackQuery
from aiogram import BaseMiddleware
from redisWork.autopostingCash.subscribe_info_cashing import redis_cash


@dataclass
class SubscribeCash:
    payment_plan: str
    end_date: str
    balance: float


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
        cash = await redis_cash.get_cash(tg_id)
        if cash:
            is_cashing = True
            subscribe_info = SubscribeCash(
                payment_plan=cash['payment_plan'],
                end_date=cash['end_date'],
                balance=cash['balance'])
        else:
            update = await redis_cash.inc_check_callback_count(tg_id=tg_id)
        data.update(subscribe_info=subscribe_info, cashing=is_cashing, update=update)

        return await handler(event, data)
