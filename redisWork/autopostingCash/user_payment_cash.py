from ..redis_init import redis_engine
import json


class UserPaymentPlansCashing:
    """CASHING FUNCTIONS"""

    @staticmethod
    async def set_cash(tg_id, payment_plan, end_date, balance, auto_pay):
        async with redis_engine as redis:
            json_data = {'payment_plan': payment_plan,
                         'end_date': end_date,
                         'balance': balance,
                         'auto_pay': auto_pay
                         }
            await redis.hset("callback_cash", tg_id, json.dumps(json_data))

    @staticmethod
    async def get_cash(tg_id):
        async with redis_engine as redis:
            cash = await redis.hget("callback_cash", tg_id)
            return json.loads(cash) if cash else None

    async def reset_auto_pay(self, auto_pay: bool, tg_id):
        async with redis_engine as redis:
            update_existing = await self.get_cash(tg_id)
            update_existing['auto_pay'] = auto_pay
            await redis.hset("callback_cash", tg_id, json.dumps(update_existing))

    async def extend_payment_plan_date(self, new_date, result_balance, tg_id):
        async with redis_engine as redis:
            update_existing = await self.get_cash(tg_id)
            update_existing["end_date"] = new_date
            update_existing["balance"] = result_balance
            update_existing['auto_pay'] = False
            await redis.hset("callback_cash", tg_id, json.dumps(update_existing))


user_payment_cash = UserPaymentPlansCashing()
