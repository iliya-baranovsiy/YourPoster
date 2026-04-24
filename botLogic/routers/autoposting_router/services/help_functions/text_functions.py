def get_subscribe_info_text(data):
    message = f"\n<b>Тариф:</b> {data.payment_plan}\n<b>Действует по:</b> {data.end_date}\n<b>Баланс:</b> {data.balance}"
    return message


error_text = "Упс, произошла, какая-то ошибка. Мы уже разбираемся в проблеме. Подожди пару минут и перезапусти бота командой /start"
