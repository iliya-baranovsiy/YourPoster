from aiogram.types import CallbackQuery, Message
from botLogic.common_keyboards.menu_kb_builder import get_main_menu


async def get_main_bot_menu(call: CallbackQuery = None, msg: Message = None):
    buttons = get_main_menu()
    if call:
        await call.message.edit_text(text="Главное меню", reply_markup=buttons)
    else:
        await msg.answer(text="Главное меню", reply_markup=buttons)
