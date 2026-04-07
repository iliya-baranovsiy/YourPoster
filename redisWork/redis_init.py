import redis.asyncio as redis
from config.configurations import settings

redis_engine = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
