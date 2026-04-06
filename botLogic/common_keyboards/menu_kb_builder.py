from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu():
    main_menu = [
        [InlineKeyboardButton(text="Автопостинг 📤", callback_data="autoposting_meu")],
        [InlineKeyboardButton(text="Пополнения 💰", callback_data="payments_menu")],
        [InlineKeyboardButton(text="FAQ ❓", callback_data="questions_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=main_menu)
