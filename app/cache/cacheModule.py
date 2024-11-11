import redis.asyncio as redis
from typing import Any, Dict, Optional

class CacheModule:
    def __init__(self, host: str, port: int, password: Optional[str] = None, db: int = 0, **kwargs):
        self.host = host
        self.port = port
        self.password = password
        self.db = db
        self.redis = None

    async def connect(self):
        self.redis = redis.Redis(
            host=self.host,
            port=self.port,
            password=self.password,
            db=self.db,
            decode_responses=True  # Automatically decode bytes to strings
        )

    async def disconnect(self):
        if self.redis:
            await self.redis.close()
            await self.redis.connection_pool.disconnect()  # Disconnect the connection pool
            self.redis = None

    async def set(self, key: str, value: Any, expire: Optional[int] = None):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.set(key, value, ex=expire)

    async def get(self, key: str) -> Optional[Any]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.get(key)

    async def delete(self, key: str):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.delete(key)

    async def exists(self, key: str) -> bool:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.exists(key)

    async def clear_all(self):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.flushdb()

    def __del__(self):
        if self.redis:
            self.redis.close()
