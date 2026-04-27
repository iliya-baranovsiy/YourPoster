import json

from ..redis_init import redis_engine


class ChannelsCache:
    async def set_channels_cache(self, tg_id, channel_tup: tuple):
        async with redis_engine as redis:
            current_data = await self.get_user_channels_cache(tg_id)
            current_data.append(channel_tup)
            await redis.set(f'user_channels:{tg_id}', json.dumps(current_data))

    @staticmethod
    async def get_user_channels_cache(tg_id):
        async with redis_engine as redis:
            channels_list = await redis.get(f"user_channels:{tg_id}")
            return json.loads(channels_list) if channels_list else []

    async def delete_channel_cache(self, tg_id, channel_id):
        async with redis_engine as redis:
            cache = await self.get_user_channels_cache(tg_id)
            if cache:
                for tup in cache:
                    if tup[0] == channel_id:
                        cache.remove(tup)
            await redis.set(f'user_channels:{tg_id}', json.dumps(cache))


channels_cache = ChannelsCache()
