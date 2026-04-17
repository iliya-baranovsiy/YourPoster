from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from .states.price_state import AgreePayPlan
from botLogic.routers.autoposting_router.services.help_functions.get_subscribe_info import get_subscribe_info
from botLogic.middleware.autoposting_middleware.subscribe_info_middleware import SubscribeInfoMiddleware, SubscribeCash
from botLogic.routers.autoposting_router.services.help_functions.text_functions import get_subscribe_info_text
from .pricing_functions.handlers_functions import pay_plan_logic
from .pricing_functions.keyboards import back_to_menu_or_pay, get_pricing_plans_menu_kb
from .pricing_functions.keyboards import question_auto_pay_kb
from database.botDb.orms.user_orm import user_db
from ..autoposting_menu import get_self_posting_menu

router = Router(name=__name__)
router.callback_query.middleware(SubscribeInfoMiddleware())


@router.callback_query(F.data == "payment_plans")
async def call_pricing_menu(call: CallbackQuery, subscribe_info: SubscribeCash, cashing: bool, update: bool,
                            state: FSMContext):
    await state.clear()
    tg_id = call.message.chat.id
    payment_data = await get_subscribe_info(subscribe_info=subscribe_info, cashing=cashing, update=update, tg_id=tg_id)
    text = get_subscribe_info_text(payment_data)
    buttons = get_pricing_plans_menu_kb(auto_pay=payment_data.auto_pay, payment_plan=payment_data.payment_plan)
    await call.message.edit_text(text='Меню тарифов, твои текущие данные:' + text, reply_markup=buttons)


@router.callback_query(F.data.startswith('plan'))
async def check_chosen_plan(call: CallbackQuery, subscribe_info: SubscribeCash, cashing: bool, update: bool,
                            state: FSMContext):
    tg_id = call.message.chat.id
    target_plan = call.data.split('_')[1]
    current_payment_data = await get_subscribe_info(subscribe_info=subscribe_info, cashing=cashing, update=update,
                                                    tg_id=tg_id)
    await pay_plan_logic(call, target_plan, current_payment_data, state)


@router.callback_query(F.data == "agree_with_pay", AgreePayPlan.agree_to_pay)
async def agree_with_payment(call: CallbackQuery, state: FSMContext, cashing: bool):
    tg_id = call.message.chat.id
    state_data = await state.get_data()
    currency = state_data.get("price")
    target_plan = state_data.get("plan")
    user_balance = float(state_data.get("balance"))
    result_user_balance = user_balance - currency
    if result_user_balance >= 0:
        buttons = question_auto_pay_kb()
        await user_db.update_user_payment_plan(tg_id=tg_id, payment_plan=target_plan, balance=result_user_balance,
                                               cashing=cashing)
        await call.message.edit_text(
            text=f"Тариф {target_plan} успешно преобретен. Желаешь ли ты включить автоматичсекое списывание ?",
            reply_markup=buttons)
    else:
        buttons = back_to_menu_or_pay()
        await call.message.edit_text("Недостаточно средств на балансе", reply_markup=buttons)


@router.callback_query(F.data.startswith("autopay"))
async def change_auto_pay(call: CallbackQuery, subscribe_info: SubscribeCash, cashing: bool, update: bool):
    tg_id = call.message.chat.id
    data = call.data.split("_")
    if data[1] == "off":
        await user_db.reset_auto_pay_value(tg_id=tg_id, auto_pay=False, cashing=cashing)
        await call.answer(text="автоматическая покупка снята", show_alert=True)
    else:
        await user_db.reset_auto_pay_value(tg_id=tg_id, auto_pay=True, cashing=cashing)
        await call.answer(text="автоматическая покупка установлена", show_alert=True)

    await get_self_posting_menu(call=call, subscribe_info=subscribe_info, cashing=cashing, update=update)
