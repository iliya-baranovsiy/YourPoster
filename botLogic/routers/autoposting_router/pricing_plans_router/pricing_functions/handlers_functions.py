from aiogram.types import CallbackQuery
from datetime import timedelta
from .date_functions import get_current_date
from ..states.price_state import AgreePayPlan
from ..keyboards.keyboards import get_agree_or_not_pay_kb, back_to_menu_or_pay, extend_or_back_kb, back_to_plans
from botLogic.routers.autoposting_router.services.keyboards.menu_keyboard import back_to_autoposting_menu

VIP_PRICE = 5.99
PRO_PRICE = 2.99


async def pay_plan_logic(call: CallbackQuery, target_plan, current_payment_data, state):
    end_date = current_payment_data.end_date
    payment_plan = current_payment_data.payment_plan
    balance = current_payment_data.balance

    if target_plan == payment_plan:
        # продление
        await extend_payment_plan(call=call, end_date=end_date, state=state, pyment_plan=payment_plan, balance=balance)
    elif target_plan == "PRO" and payment_plan == "VIP":
        await logic_with_max_plan(call=call)
    elif target_plan == "VIP" and payment_plan == "PRO":
        await buy_payment_plan(call=call, state=state, price=VIP_PRICE, target_plan=target_plan, balance=balance,
                               change=True)
    elif target_plan == "VIP" and float(balance) - VIP_PRICE >= 0:
        await buy_payment_plan(call=call, state=state, price=VIP_PRICE, target_plan=target_plan, balance=balance)
    elif target_plan == "PRO" and float(balance) - PRO_PRICE >= 0:
        await buy_payment_plan(call=call, state=state, price=PRO_PRICE, target_plan=target_plan, balance=balance)
    else:
        await small_balance(call=call)


async def extend_payment_plan(call, end_date: str, state, pyment_plan, balance):
    price = VIP_PRICE if pyment_plan == "VIP" else PRO_PRICE
    result_balance = float(balance) - price
    if result_balance >= 0:
        buttons = extend_or_back_kb()
        await state.set_state(AgreePayPlan.agree_to_extend)
        date_to_db = get_current_date(end_date)
        await state.update_data(end_date=date_to_db + timedelta(days=31), result_balance=result_balance)
        text = f"Выбранный тариф уже дейсвует по <b>{end_date}</b>Хочешь продлить тариф за {price}?"
    else:
        buttons = back_to_plans()
        text = f"Выбранный тариф уже дейсвует по <b>{end_date}</b>"
    await call.message.edit_text(
        text=text,
        reply_markup=buttons)


async def logic_with_max_plan(call):
    buttons = back_to_autoposting_menu()
    await call.message.edit_text(text="У тебя уже куплен максимальный тариф", reply_markup=buttons)


async def buy_payment_plan(call, state, price, target_plan, balance, change=False):
    buttons = get_agree_or_not_pay_kb()
    await state.set_state(AgreePayPlan.agree_to_pay)
    await state.update_data(price=price, plan=target_plan, balance=balance)
    if change:
        text = f"Ты уверен, что хочешь перейти на тариф {target_plan} и потратить {price}?"
    else:
        text = f"Ты уверен, что хочешь потратить {price}$ и преобрести тариф {target_plan}"
    await call.message.edit_text(
        text=text, reply_markup=buttons)


async def small_balance(call):
    buttons = back_to_menu_or_pay()
    await call.message.edit_text("Недостаточно средств на балансе", reply_markup=buttons)
