from typing import Callable, Dict, Any, Awaitable
from dataclasses import dataclass
from aiogram.types import Message
from aiogram import BaseMiddleware
from redisWork.app_casing.user_id_cashing import user_id_cashing

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
        self.exist = await user_id_cashing.check_user_existing(tg_id=str(event.chat.id))
        data.update(
            existing=CheckUserExisting(self.exist)
        )
        return await handler(event, data)
