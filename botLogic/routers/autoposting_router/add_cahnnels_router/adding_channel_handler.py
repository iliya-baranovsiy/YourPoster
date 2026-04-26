from aiogram import Router, F
from aiogram.handlers.callback_query import CallbackQuery
from aiogram.handlers.message import Message
from aiogram.fsm.context import FSMContext
from .keyboards.channels_list_kb import get_channels_buttons
from .states.add_channel_state import AddChannelState
from .keyboards.channels_list_kb import back_to_channels_menu
from .utils.functions.check_member import is_member

router = Router(name=__name__)


@router.callback_query(F.data == "my_channels")
async def user_channels_list(call: CallbackQuery):
    channels = []
    ability_to_add = True
    buttons = get_channels_buttons(channels, ability_to_add)
    # add text info about channels count and ability to add and payment plan
    await call.message.edit_text("Твои каналы", reply_markup=buttons)


@router.callback_query(F.data == "add_channel")
async def add_channel(call: CallbackQuery, state: FSMContext):
    buttons = back_to_channels_menu()
    await call.message.edit_text("Добавь бота в канал и перешли любой пост из канала мне сюда", reply_markup=buttons)
    await state.set_state(AddChannelState.wait_repost)


@router.message(AddChannelState.wait_repost)
async def get_post(msg: Message):
    if msg.forward_from_chat and msg.forward_from_chat.type == "channel":
        await is_member(chat_id=msg.forward_from_chat.id)
