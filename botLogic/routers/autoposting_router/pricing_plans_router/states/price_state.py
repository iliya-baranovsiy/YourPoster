from aiogram.fsm.state import StatesGroup, State


class AgreePayPlan(StatesGroup):
    agree_to_pay = State()
