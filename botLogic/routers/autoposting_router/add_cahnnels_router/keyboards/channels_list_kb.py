from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_channels_buttons(channels: list, add: bool):
    buttons = []
    if channels:
        for channel in channels:
            buttons.append([InlineKeyboardButton(text=channel, callback_data=channel)])
    if add:
        buttons.append([InlineKeyboardButton(text="Добавить канал", callback_data="add_channel")])
    buttons.append([InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")])
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_channels_menu():
    buttons = [
        [InlineKeyboardButton(text="Назад", callback_data="my_channels")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
