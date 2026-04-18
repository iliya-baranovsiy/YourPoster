from ..redis_init import redis_engine


class UserIdCashing:
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


user_id_cashing = UserIdCashing()
