import asyncio

from .redis_init import redis_engine


class RedisQueries:
    async def set_user(self, tg_id):
        async with redis_engine as redis:
            await redis.sadd('tg_users', tg_id)

    async def check_user_existing(self, tg_id):
        async with redis_engine as redis:
            result = await redis.sismember('tg_users', tg_id)
            return result

    async def clear_users_set(self):
        async with redis_engine as redis:
            await redis.delete('tg_users')


redis_q = RedisQueries()
