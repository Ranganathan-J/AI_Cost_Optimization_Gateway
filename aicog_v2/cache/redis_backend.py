import logging
import json
from typing import Optional
import redis.asyncio as redis
from aicog_v2.core.interfaces import AICache

logger = logging.getLogger(__name__)

class RedisCache(AICache):
    def __init__(self, host: str = '127.0.0.1', port: int = 6379, db: int = 0, password: Optional[str] = None):
        self.client = redis.Redis(host=host, port=port, db=db, password=password, decode_responses=True)

    async def get(self, key: str) -> Optional[str]:
        try:
            return await self.client.get(key)
        except Exception as e:
            logger.debug(f"Redis Cache GET failed: {e}")
            return None

    async def set(self, key: str, value: str, ttl: int = 3600):
        try:
            await self.client.setex(key, ttl, value)
        except Exception as e:
            logger.debug(f"Redis Cache SET failed: {e}")
            pass
