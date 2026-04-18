from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from botLogic.middleware.autoposting_middleware.subscribe_info_middleware import SubscribeInfoMiddleware, SubscribeCash
from ..autoposting_router.services.help_functions.text_functions import get_subscribe_info_text
from .services.keyboards.auto_posting_kb import get_self_posting_menu_kb
from .services.help_functions.get_subscribe_info import get_subscribe_info

router = Router(name=__name__)
router.callback_query.middleware(SubscribeInfoMiddleware())


@router.callback_query(F.data == "autoposting_menu")
async def get_self_posting_menu(call: CallbackQuery, subscribe_info: SubscribeCash, cashing: bool, update: bool,
                                state: FSMContext):
    await state.clear()
    tg_id = call.message.chat.id
    keyboard = get_self_posting_menu_kb()
    payment_data = await get_subscribe_info(subscribe_info=subscribe_info, cashing=cashing, update=update, tg_id=tg_id)
    text = get_subscribe_info_text(payment_data)
    await call.message.edit_text(text='Меню автопостинга' + text, reply_markup=keyboard)
