from botLogic.bot_services.bot_instance import bot
from database.botDb.channelsDb.channels_orm import channels_orm
from .AddChannelStatus import AddChannelStatus
from aiogram.types.chat import Chat


async def can_post(chat_id: int):
    try:
        message = await bot.send_message(chat_id=chat_id, text=".", disable_notification=True)
        await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        return AddChannelStatus.OK
    except:
        return AddChannelStatus.NO_ACCESS


async def is_valid_to_add(forward: Chat):
    if not forward or forward.type != "channel":
        return AddChannelStatus.NOT_CHANNEL
    exists = await channels_orm.is_channel_exists(forward.id)
    if exists:
        return AddChannelStatus.ALREADY_EXISTS
    return await can_post(forward.id)
