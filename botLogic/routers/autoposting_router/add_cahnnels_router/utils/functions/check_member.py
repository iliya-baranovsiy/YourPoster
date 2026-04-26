from botLogic.bot_services.bot_instance import bot


async def is_member(chat_id):
    me = await bot.get_me()
    try:
        member = await bot.get_chat_member(chat_id=chat_id, user_id=me.id)
        if member.status == "administrator":
            return True
    except:
        return False
