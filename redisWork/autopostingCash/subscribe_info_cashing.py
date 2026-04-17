from ..redis_init import redis_engine
import json


class RedisCashing:
    """VALIDATE CASHING"""

    async def inc_check_callback_count(self, tg_id) -> bool:
        async with redis_engine as redis:
            current_count = await self.get_callback_count(tg_id)
            if not current_count:
                await redis.hset('callback_cash_count', tg_id, 1)
                return False
            elif current_count >= 6:
                await self.delete_user_callback_count(tg_id)
                return True
            else:
                await redis.hset('callback_cash_count', tg_id, current_count + 1)
                return False

    @staticmethod
    async def get_callback_count(tg_id):
        async with redis_engine as redis:
            count = await redis.hget('callback_cash_count', tg_id)
            return int(count) if count else None

    @staticmethod
    async def delete_user_callback_count(tg_id):
        async with redis_engine as redis:
            await redis.hdel('callback_cash_count', tg_id)

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

    """DROP FUNCTIONS"""

    @staticmethod
    async def drop_counter():
        # temporary
        async with redis_engine as redis:
            await redis.delete("callback_cash_count")

    @staticmethod
    async def drop_cash():
        # temporary
        async with redis_engine as redis:
            await redis.delete("callback_cash")

    @staticmethod
    async def get_all():
        # delete
        async with redis_engine as redis:
            result = await redis.hgetall("callback_cash")
            return result


redis_cash = RedisCashing()
