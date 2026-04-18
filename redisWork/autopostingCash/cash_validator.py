from ..redis_init import redis_engine


class CashValidator:
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


cash_validator = CashValidator()
