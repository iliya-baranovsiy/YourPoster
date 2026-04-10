from aiogram.types import CallbackQuery
from aiogram import Router, F
from botLogic.common_functions.menu_handlers_functions import get_main_bot_menu

router = Router(name=__name__)


@router.callback_query(F.data == "main_menu")
async def back_to_main_menu(call: CallbackQuery):
    await get_main_bot_menu(call=call)
