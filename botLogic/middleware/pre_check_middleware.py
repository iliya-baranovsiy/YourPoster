from typing import Callable, Dict, Any, Awaitable
from dataclasses import dataclass
from aiogram.types import Message
from aiogram import BaseMiddleware
from redisWork.redis_functions import redis_q


@dataclass
class CheckUserExisting:
    exists: bool


class CheckUserMiddleware(BaseMiddleware):
    def __init__(self):
        self.exist = False

    async def __call__(
            self,
            handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
            event: Message,
            data: Dict[str, Any]
    ) -> Any:
        self.exist = await redis_q.check_user_existing(tg_id=str(event.chat.id))
        data.update(
            existing=CheckUserExisting(self.exist)
        )
        return await handler(event, data)
