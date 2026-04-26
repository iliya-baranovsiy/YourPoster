from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware
from database.botDb.channelsDb.channels_orm import channels_orm
from botLogic.routers.autoposting_router.add_cahnnels_router.utils.db_help_functions.get_ability_to_add import \
    get_ability_to_add


class ChannelMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        tg_id = event.from_user.id
        channels_list = await channels_orm.get_users_channels(tg_id)
        ability = await get_ability_to_add(tg_id=tg_id, channels_list=channels_list)
        data.update(channels_list=channels_list, ability_to_add=ability[0], payment_plan=ability[1])
        return await handler(event, data)
