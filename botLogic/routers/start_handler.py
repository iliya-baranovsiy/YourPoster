from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from database.commonDb.user_orm import user_orm
from botLogic.middleware.pre_check_middleware import CheckUserMiddleware, CheckUserExisting
from redisWork.app_casing.user_id_cashing import user_id_cashing
from ..common_functions.menu_handlers_functions import get_main_bot_menu

router = Router(name=__name__)
router.message.middleware(CheckUserMiddleware())


@router.message(CommandStart())
async def start_message(msg: Message, existing: CheckUserExisting, state: FSMContext):
    if existing.exists:
        await msg.answer('Hello message')
        await get_main_bot_menu(msg=msg)
        await state.clear()
    else:
        tg_id = msg.chat.id
        username = '@' + msg.chat.username
        await user_orm.create_user(tg_id=tg_id, username=username)
        await user_id_cashing.set_user(str(tg_id))
        await msg.answer('Hello message')
        await get_main_bot_menu(msg=msg)
