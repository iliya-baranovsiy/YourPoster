from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def get_pricing_plans_menu_kb(auto_pay: bool, payment_plan: str):
    if payment_plan == "STANDART":
        buttons = [
            [InlineKeyboardButton(text="VIP", callback_data="plan_VIP")],
            [InlineKeyboardButton(text="PRO", callback_data="plan_PRO")],
            [InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")]
        ]
        return InlineKeyboardMarkup(inline_keyboard=buttons)
    if auto_pay:
        buttons = [
            [InlineKeyboardButton(text="VIP", callback_data="plan_VIP")],
            [InlineKeyboardButton(text="PRO", callback_data="plan_PRO")],
            [InlineKeyboardButton(text="Выключить автосписывание", callback_data="autopay_off")],
            [InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")]
        ]
    else:
        buttons = [
            [InlineKeyboardButton(text="VIP", callback_data="plan_VIP")],
            [InlineKeyboardButton(text="PRO", callback_data="plan_PRO")],
            [InlineKeyboardButton(text="Включить автосписывание", callback_data='autopay_in')],
            [InlineKeyboardButton(text="Назад", callback_data="autoposting_menu")]
        ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def get_agree_or_not_pay_kb():
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


def question_auto_pay_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data="autopay_in"),
            InlineKeyboardButton(text="Нет", callback_data="autoposting_menu")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)


def extend_or_back_kb():
    buttons = [
        [
            InlineKeyboardButton(text="Да", callback_data="extend_payment_plan_callback"),
            InlineKeyboardButton(text="Нет", callback_data="payment_plans")
        ]
    ]
    return InlineKeyboardMarkup(inline_keyboard=buttons)
