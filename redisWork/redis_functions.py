import asyncio
import json

from .redis_init import redis_engine


class RedisQueries:
    @staticmethod
    async def set_user(tg_id):
        async with redis_engine as redis:
            await redis.sadd('tg_users', tg_id)

    @staticmethod
    async def check_user_existing(tg_id):
        async with redis_engine as redis:
            result = await redis.sismember('tg_users', tg_id)
            return result

    @staticmethod
    async def clear_users_set():
        async with redis_engine as redis:
            await redis.delete('tg_users')


class RedisCashing:
    @staticmethod
    async def set_callback_count(tg_id, count=0):
        async with redis_engine as redis:
            await redis.hset('callback_cash_count', tg_id, count)

    @staticmethod
    async def get_callback_count(tg_id):
        async with redis_engine as redis:
            count = await redis.hget('callback_cash_count', tg_id)
            return int(count) if count else None

    @staticmethod
    async def delete_user_callback_count(tg_id):
        async with redis_engine as redis:
            await redis.hdel('callback_cash_count', tg_id)

    @staticmethod
    async def set_cash(tg_id, payment_plan, end_date, balance):
        async with redis_engine as redis:
            json_data = {'payment_plan': payment_plan,
                         'end_date': end_date,
                         'balance': balance
                         }
            await redis.hset("callback_cash", tg_id, json.dumps(json_data))

    @staticmethod
    async def get_cash(tg_id):
        async with redis_engine as redis:
            cash = await redis.hget("callback_cash", tg_id)
            return json.loads(cash)

    @staticmethod
    async def drop_counter():
        async with redis_engine as redis:
            await redis.delete("callback_cash_count")

    @staticmethod
    async def drop_cash():
        async with redis_engine as redis:
            await redis.delete("callback_cash")


redis_q = RedisQueries()
redis_cash = RedisCashing()
