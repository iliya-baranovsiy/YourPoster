from aiogram.types import CallbackQuery
from .keyboards import get_agree_or_not_kb, back_to_plans, back_to_menu_or_pay
from ..states.price_state import AgreePayPlan


async def pay_plan_logic(call: CallbackQuery, target_plan, current_payment_data, state):
    VIP_PRICE = 5.99
    PRO_PRICE = 2.99
    if target_plan == current_payment_data.payment_plan:
        buttons = back_to_plans()
        await call.message.edit_text(text=f"Выбранный тариф уже дейсвует по <b>{current_payment_data.end_date}</b>",
                                     reply_markup=buttons)
    elif target_plan == "VIP" and float(current_payment_data.balance) - VIP_PRICE >= 0:
        buttons = get_agree_or_not_kb()
        await state.set_state(AgreePayPlan.agree_to_pay)
        await state.update_data(price=VIP_PRICE, plan=target_plan, balance=current_payment_data.balance)
        await call.message.edit_text(
            text=f"Ты уверен, что хочешь потратить {VIP_PRICE}$ и преобрести тариф {target_plan}", reply_markup=buttons)
    elif target_plan == "PRO" and float(current_payment_data.balance) - PRO_PRICE >= 0:
        buttons = get_agree_or_not_kb()
        await state.set_state(AgreePayPlan.agree_to_pay)
        await state.update_data(price=PRO_PRICE, plan=target_plan, balance=current_payment_data.balance)
        await call.message.edit_text(
            text=f"Ты уверен, что хочешь потратить {PRO_PRICE}$ и преобрести тариф {target_plan}", reply_markup=buttons)
    else:
        buttons = back_to_menu_or_pay()
        await call.message.edit_text("Недостаточно средств на балансе", reply_markup=buttons)
