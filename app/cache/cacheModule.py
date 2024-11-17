import redis.asyncio as redis
from typing import Any, Optional, List, Dict, Set


class CacheModule:
    def __init__(
        self,
        host: str,
        port: int,
        user: str,
        password: Optional[str] = None,
        debug_mode: Optional[bool] = False,
        **kwargs,
    ):
        self.host = host
        self.port = port
        self.password = password
        self.user = user
        self.redis = None
        self.debug_mode = debug_mode

    async def connect(self):
        print("Trying to connect to Redis")

        self.redis = redis.Redis(
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            ssl=not self.debug_mode,
            ssl_cert_reqs=None,
            decode_responses=True,
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

    # New methods for hash operations

    async def hset(self, key: str, field: str, value: Any):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.hset(key, field, value)

    async def hget(self, key: str, field: str) -> Optional[Any]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.hget(key, field)

    async def hdel(self, key: str, field: str):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.hdel(key, field)

    async def hgetall(self, key: str) -> Dict[str, Any]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.hgetall(key)

    async def hkeys(self, key: str) -> List[str]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.hkeys(key)

    async def hvals(self, key: str) -> List[Any]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.hvals(key)

    # New methods for set operations

    async def sadd(self, key: str, *members: str):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.sadd(key, *members)

    async def smembers(self, key: str) -> Set[str]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.smembers(key)

    async def srem(self, key: str, *members: str):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.srem(key, *members)

    async def scard(self, key: str) -> int:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.scard(key)

    # New methods for list operations (if needed)

    async def lpush(self, key: str, *values: Any):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.lpush(key, *values)

    async def rpush(self, key: str, *values: Any):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.rpush(key, *values)

    async def lrange(self, key: str, start: int, end: int) -> List[Any]:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.lrange(key, start, end)

    async def lrem(self, key: str, count: int, value: Any):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.lrem(key, count, value)

    # Additional methods for better cache management

    async def expire(self, key: str, time: int):
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        await self.redis.expire(key, time)

    async def ttl(self, key: str) -> int:
        if not self.redis:
            raise ConnectionError("CacheModule is not connected.")
        return await self.redis.ttl(key)
