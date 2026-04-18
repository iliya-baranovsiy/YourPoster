from botLogic.middleware.autoposting_middleware.subscribe_info_middleware import SubscribeCash
from database.botDb.paymentPlansDB.payment_orm import payment_orm
from redisWork.autopostingCash.user_payment_cash import user_payment_cash


async def get_subscribe_info(subscribe_info: SubscribeCash | None, cashing: bool, update: bool, tg_id):
    if cashing:
        return subscribe_info
    else:
        payment_data = await payment_orm.get_user_payment_plan_info(tg_id)
        if update:
            await user_payment_cash.set_cash(tg_id=tg_id, payment_plan=str(payment_data.payment_plan),
                                      end_date=str(payment_data.end_date),
                                      balance=float(payment_data.balance),
                                      auto_pay=payment_data.auto_pay)
        return payment_data
