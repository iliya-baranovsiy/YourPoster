from aiogram import Router, F
from aiogram.types import CallbackQuery
from database.botDb.orms.user_orm import user_db
from botLogic.middleware.autoposting_middleware.subscribe_info_middleware import SubscribeInfoMiddleware, SubscribeCash
from .help_functions.text_functions import get_subscribe_info_text
from redisWork.autopostingCash.subscribe_info_cashing import redis_cash

router = Router(name=__name__)
router.callback_query.middleware(SubscribeInfoMiddleware())


@router.callback_query(F.data == "autoposting_menu")
async def get_self_posting_menu(call: CallbackQuery, subscribe_info: SubscribeCash, cashing: bool, update: bool,
                                ):
    tg_id = call.message.chat.id
    if cashing:
        text = get_subscribe_info_text(subscribe_info)
    else:
        payment_data = await user_db.get_user_payment_plan_info(tg_id)
        if update:
            await redis_cash.set_cash(tg_id=tg_id, payment_plan=str(payment_data.payment_plan),
                                      end_date=str(payment_data.end_date),
                                      balance=float(payment_data.balance))
        text = get_subscribe_info_text(payment_data)
    await call.message.edit_text(text)
