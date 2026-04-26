from database.botDb.paymentPlansDB.payment_orm import payment_orm
from redisWork.autopostingCash.user_payment_cash import user_payment_cash
from .payment_plans_limits import PaymentLimit
import asyncio


async def get_ability_to_add(tg_id: int, channels_list: list):
    cash = await user_payment_cash.get_cash(tg_id)
    if cash:
        payment_plan = cash['payment_plan']
    else:
        payment_data = await payment_orm.get_user_payment_plan_info(tg_id)
        payment_plan = payment_data.payment_plan
    ability_count = PaymentLimit[payment_plan].value
    return True if ability_count > len(channels_list) else False, payment_plan
