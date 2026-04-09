from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.botDb.orms.user_orm import user_db
from botLogic.middleware.autoposting_middleware.subscribe_info_middleware import SubscribeInfoMiddleware, SubscribeCash
from .help_functions.text_functions import get_subscribe_info_text
from redisWork.autopostingCash.subscribe_info_cashing import redis_cash

router = Router(name=__name__)
router.message.middleware(SubscribeInfoMiddleware())


@router.callback_query(F.data == "autoposting_menu")
async def get_self_posting_menu(call: CallbackQuery, **kwargs
                                ):
    data = kwargs.get('data', {})
    cashing = data.get('cashing')
    update = data.get('update')
    subscribe_info = data.get('subscribe_info')
    tg_id = call.message.chat.id
    print(cashing)
    text = 'test'
    if cashing:
        payment_plan = subscribe_info.payment_plan
        end_date = subscribe_info.end_date
        balance = subscribe_info.balance
        text = get_subscribe_info_text(payment_plan=payment_plan, end_date=end_date, balance=balance)
    else:
        payment_data = await user_db.get_user_payment_plan_info(tg_id)
        payment_plan = payment_data.payment_plan,
        end_date = payment_data.end_date,
        balance = payment_data.balance
        if update:
            await redis_cash.set_cash(tg_id=tg_id, payment_plan=payment_plan, end_date=end_date, balance=balance)
            text = get_subscribe_info_text(payment_plan=payment_plan, end_date=end_date, balance=balance)
    await call.message.edit_text(text)
