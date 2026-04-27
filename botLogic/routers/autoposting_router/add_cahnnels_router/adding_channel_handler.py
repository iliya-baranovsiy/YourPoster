from aiogram import Router, F
from aiogram.handlers.callback_query import CallbackQuery
from aiogram.handlers.message import Message
from aiogram.fsm.context import FSMContext
from .keyboards.channels_list_kb import get_channels_buttons
from .states.add_channel_state import AddChannelState
from .keyboards.channels_list_kb import back_to_channels_menu
from .utils.functions.check_member import is_valid_to_add
from database.botDb.channelsDb.channels_orm import channels_orm
from .utils.functions.AddChannelStatus import AddChannelStatus
from botLogic.middleware.autoposting_middleware.channels_middleware import ChannelMiddleware

router = Router(name=__name__)
router.callback_query.middleware(ChannelMiddleware())


@router.callback_query(F.data == "my_channels")
async def user_channels_list(call: CallbackQuery, channels_list: list, ability_to_add: bool, payment_plan: str,
                             ability_count: int,
                             state: FSMContext):
    await state.clear()
    buttons = get_channels_buttons(channels_list, ability_to_add)
    await call.message.edit_text(
        f"Твой тариф: {payment_plan}\nДоступно каналов для привязки: {ability_count}\nТвои каналы",
        reply_markup=buttons)


@router.callback_query(F.data == "add_channel")
async def add_channel(call: CallbackQuery, state: FSMContext):
    buttons = back_to_channels_menu()
    await call.message.edit_text("Добавь бота в канал и перешли любой пост из канала мне сюда", reply_markup=buttons)
    await state.set_state(AddChannelState.wait_repost)


@router.message(AddChannelState.wait_repost)
async def get_post(msg: Message, state: FSMContext):
    buttons = back_to_channels_menu()

    user_id = msg.chat.id
    forwarded = msg.forward_from_chat
    status = await is_valid_to_add(forwarded)

    if status == AddChannelStatus.OK:
        channel_id = forwarded.id
        channel_title = forwarded.title
        await channels_orm.add_user_channel(owner_id=user_id, channel_id=channel_id, title=channel_title)
        await msg.answer("Канал успешно привязан", reply_markup=buttons)
        await state.clear()
    elif status == AddChannelStatus.NOT_CHANNEL:
        await msg.answer("Место откуда ты пересылаешь не является каналом. Попробуй заново", reply_markup=buttons)
    elif status == AddChannelStatus.ALREADY_EXISTS:
        await msg.answer("Данный канал уже привязан. Попробуй заново", reply_markup=buttons)
    elif status == AddChannelStatus.NO_ACCESS:
        await msg.answer("Предоставь боту соответствующие права и добавь его в канал. Попробуй заново",
                         reply_markup=buttons)
    else:
        await msg.answer("Что-то пошло не так. Попробуй заново",
                         reply_markup=buttons)
