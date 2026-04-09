from typing import Callable, Dict, Any, Awaitable
from dataclasses import dataclass
from aiogram.types import Message, CallbackQuery
from aiogram import BaseMiddleware
from redisWork.autopostingCash.subscribe_info_cashing import redis_cash


@dataclass
class SubscribeCash:
    payment_plan: str
    end_date: str
    balance: float


class SubscribeInfoMiddleware(BaseMiddleware):
    is_cashing = False
    update: bool

    async def __call__(
            self,
            handler: Callable[[CallbackQuery, Dict[str, Any]], Awaitable[Any]],
            event: CallbackQuery,
            data: Dict[str, Any]
    ) -> Any:
        tg_id = CallbackQuery.message.chat.id
        cash = await redis_cash.get_cash(tg_id)
        if cash:
            self.is_cashing = True
            data.update(subscribe_info=SubscribeCash(
                payment_plan=cash['payment_plan'],
                end_date=cash['end_date'],
                balance=cash['balance']
            ),
                cashing=self.is_cashing,
                update=False
            )
        else:
            self.update = await redis_cash.inc_check_callback_count(tg_id=tg_id)
            data.update(cashing=self.is_cashing, update=self.update, subscribe_info=None)
            print('increment')

        return await handler(event, data)
