from typing import Callable, Dict, Any, Awaitable
from aiogram.types import TelegramObject
from aiogram import BaseMiddleware
from database.botDb.channelsDb.channels_orm import channels_orm
from botLogic.routers.autoposting_router.add_cahnnels_router.utils.db_help_functions.get_ability_to_add import \
    get_ability_to_add
from redisWork.autopostingCash.user_payment_cash import user_payment_cash
from redisWork.autopostingCash.channels_cash import channels_cache


class ChannelMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        tg_id = event.from_user.id

        payment_cash_data = await user_payment_cash.get_cash(tg_id)
        channels_cash_data = await channels_cache.get_user_channels_cache(tg_id)
        if payment_cash_data and channels_cash_data:
            channels = channels_cash_data
            payment_plan = payment_cash_data['payment_plan']
        else:
            user_data = await channels_orm.get_user_base_parameters(tg_id)
            channels = user_data.channels
            payment_plan = user_data.payment_plan

        ability = get_ability_to_add(channels_list=channels, payment_plan=payment_plan)
        data.update(channels_list=channels, ability_to_add=ability[0], payment_plan=ability[1],
                    ability_count=ability[2])
        return await handler(event, data)
