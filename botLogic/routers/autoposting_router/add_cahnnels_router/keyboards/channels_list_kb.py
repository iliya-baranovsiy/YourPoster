from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_channels_buttons(channels: list, add: bool) -> InlineKeyboardMarkup:
    buttons = []
    if channels:
        for tup in channels:
            buttons.append([InlineKeyboardButton(text=tup[1], callback_data='channel_' + str(tup[0]))])
    if add:
        buttons.append([InlineKeyboardButton(text="Добавить канал", callback_data="add_channel")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_channels_menu() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="my_channels")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
