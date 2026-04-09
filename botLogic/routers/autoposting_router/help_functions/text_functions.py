def get_subscribe_info_text(payment_plan, end_date, balance):
    message = f"Меню автопостинга\n<b>Тариф:</b> {payment_plan}\n"
    f"<b>Действует по:</b> {end_date}\n"
    f"<b>Баланс:</b> {balance}"
    return message
