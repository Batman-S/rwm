from redis.asyncio import Redis
from redis import asyncio as aioredis
from app.config import settings
import logging

logger = logging.getLogger("RedisManager")


class RedisManager:
    def __init__(self, redis_url: str):
        self._redis_url = redis_url
        self._redis: Redis | None = None

    async def connect(self):
        if self._redis is None:
            try:
                self._redis = aioredis.from_url(self._redis_url, decode_responses=True)
                logger.info("Connected to Redis.")
            except Exception as e:
                logger.error(f"Failed to connect to Redis: {str(e)}")
                raise RuntimeError("Redis connection failed.") from e

    async def close(self):
        if self._redis:
            try:
                await self._redis.close()
                logger.info("Redis connection closed.")
            except Exception as e:
                logger.error(f"Failed to close Redis connection: {str(e)}")

    async def get_client(self) -> Redis:
        if not self._redis:
            await self.connect()
        return self._redis


redis_manager = RedisManager(settings.REDIS_URL)


# Dependency Injection
async def get_redis_client() -> Redis:
    return await redis_manager.get_client()
