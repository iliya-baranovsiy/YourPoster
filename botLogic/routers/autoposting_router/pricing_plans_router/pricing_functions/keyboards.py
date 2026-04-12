from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_pricing_plans_menu_kb():
    buttons = [
        [InlineKeyboardButton(text="PRO", callback_data="plan_PRO")],
        [InlineKeyboardButton(text="VIP", callback_data="plan_VIP")],
        [InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_agree_or_not_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data="agree_with_pay"),
            InlineKeyboardButton(text="Нет", callback_data="payment_plans")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_plans():
    buttons = [
        [InlineKeyboardButton(text='Назад', callback_data="payment_plans")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_to_menu_or_pay():
    buttons = [
        [InlineKeyboardButton(text="Пополнить", callback_data="update_balance")],
        [InlineKeyboardButton(text='Назад', callback_data="payment_plans")]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
