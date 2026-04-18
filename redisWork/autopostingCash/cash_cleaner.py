from ..redis_init import redis_engine


class CashCleaner:
    """Cleaning payments cash from automatic posting"""

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


cash_cleaner = CashCleaner()
