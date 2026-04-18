from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_self_posting_menu_kb():
    buttons = [
        [InlineKeyboardButton(text="Мои каналы", callback_data="my_channels")],
        [InlineKeyboardButton(text="Тарифы", callback_data="payment_plans")],
        [InlineKeyboardButton(text="Узнать Id канала", callback_data="get_channel_id")],
        [InlineKeyboardButton(text="Назад", callback_data="main_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_autoposting_menu():
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="payment_plans")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
