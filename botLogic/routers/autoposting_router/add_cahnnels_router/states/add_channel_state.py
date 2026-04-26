from aiogram.fsm.state import State, StatesGroup


class AddChannelState(StatesGroup):
    wait_repost = State()
