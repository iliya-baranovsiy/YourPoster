from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.botDb.orms.user_orm import user_db

router = Router(name=__name__)


@router.callback_query(F.data == "autoposting_menu")
async def get_self_posting_menu(call: CallbackQuery):
    tg_id = call.message.chat.id
    payment_data = await user_db.get_user_payment_plan_info(tg_id)
    await call.message.edit_text(f"Меню автопостинга\nТариф: {payment_data.payment_plan}\n"
                              f"Срок действия {payment_data.activate_date} - {payment_data.activate_date}\n"
                              f"Баланс {payment_data.balance}")
