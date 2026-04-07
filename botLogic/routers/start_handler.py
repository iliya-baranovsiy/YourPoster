from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from botLogic.common_keyboards.menu_kb_builder import get_main_menu
from database.botDb.orms.user_orm import user_db
from botLogic.middleware.pre_check_middleware import CheckUserMiddleware, CheckUserExisting
from redisWork.redis_functions import redis_q

router = Router(name=__name__)
router.message.middleware(CheckUserMiddleware())


@router.message(CommandStart())
async def start_message(msg: Message, existing: CheckUserExisting):
    buttons = get_main_menu()
    if existing.exists:
        await msg.answer('Hello message', reply_markup=buttons)
    else:
        tg_id = msg.chat.id
        username = '@' + msg.chat.username
        await user_db.create_user(tg_id=tg_id, username=username)
        await redis_q.set_user(str(tg_id))
        await msg.answer('Hello message', reply_markup=buttons)
