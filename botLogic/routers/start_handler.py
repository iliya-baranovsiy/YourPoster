from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from botLogic.common_keyboards.menu_kb_builder import get_main_menu
from database.botDb.orms.user_orm import user_db
from botLogic.middleware.pre_check_middleware import CheckUserMiddleware, CheckUserExisting
from redisWork.autopostingCash.user_id_cashing import redis_q
from ..common_functions.menu_handlers_functions import get_main_bot_menu

router = Router(name=__name__)
router.message.middleware(CheckUserMiddleware())


@router.message(CommandStart())
async def start_message(msg: Message, existing: CheckUserExisting):
    if existing.exists:
        await msg.answer('Hello message')
        await get_main_bot_menu(msg=msg)
    else:
        tg_id = msg.chat.id
        username = '@' + msg.chat.username
        await user_db.create_user(tg_id=tg_id, username=username)
        await redis_q.set_user(str(tg_id))
        await msg.answer('Hello message')
        await get_main_bot_menu(msg=msg)
