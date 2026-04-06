from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from botLogic.common_keyboards.menu_kb_builder import get_main_menu
from database.botDb.usersDb.user_orm import user_db

router = Router(name=__name__)


@router.message(CommandStart())
async def start_message(msg: Message):
    tg_id = msg.chat.id
    username = '@' + msg.chat.username
    await user_db.create_user(tg_id=tg_id, username=username)
    buttons = get_main_menu()
    await msg.answer('Hello message', reply_markup=buttons)
