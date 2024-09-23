from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, HTTPException, Path

from app.config import settings
from app.exchanges.models import Exchange, ExchangeReply


class Storage(ABC):
    @abstractmethod
    async def save_exchange(self, exchange: Exchange) -> None:
        """Save or update an exchange."""

    @abstractmethod
    async def get_exchange(self, id: str) -> Exchange | None:
        """Get an exchange by its ID, or None if it doesn't exist."""

    @abstractmethod
    async def push_reply(self, exchange: Exchange, reply: ExchangeReply) -> None:
        """Add a new reply to an exchange."""

    @abstractmethod
    async def get_replies(self, exchange_id: str) -> list[ExchangeReply]:
        """Get all replies for an exchange.

        Returns an empty list if the exchange doesn't exist.
        """

    @abstractmethod
    async def delete_exchange(self, id: str) -> None:
        """Delete an exchange and any replies by its ID."""


class MemoryStorage(Storage):
    def __init__(self) -> None:
        self._exchanges: dict[str, str] = {}
        self._exchange_replies: defaultdict[str, list[str]] = defaultdict(list)

    async def save_exchange(self, exchange: Exchange):
        self._exchanges[exchange.id] = exchange.model_dump_json()

    async def get_exchange(self, id: str):
        exchange = self._exchanges.get(id)
        if exchange is None:
            return None
        return Exchange.model_validate_json(exchange)

    async def push_reply(self, exchange: Exchange, reply: ExchangeReply):
        self._exchange_replies[reply.exchange_id].append(reply.model_dump_json())

    async def get_replies(self, exchange_id: str):
        replies = self._exchange_replies.get(exchange_id, [])
        return [ExchangeReply.model_validate_json(reply) for reply in replies]

    async def delete_exchange(self, id: str):
        if id in self._exchanges:
            del self._exchanges[id]
            del self._exchange_replies[id]


class RedisStorage(Storage):
    """Storage backend using Redis.

    This stores `Exchange` objects as JSON strings at `exchange:{id}`.
    The corresponding replies are stored in a list at `exchange_replies:{id}`,
    in order of creation.
    """

    def __init__(self, redis: redis.Redis):
        self._redis = redis

    async def save_exchange(self, exchange: Exchange):
        await self._redis.set(
            f"exchange:{exchange.id}",
            exchange.model_dump_json(),
            exat=exchange.expire_at,
        )

    async def get_exchange(self, id: str):
        data = await self._redis.get(f"exchange:{id}")
        return Exchange.model_validate_json(data) if data else None

    async def push_reply(self, exchange: Exchange, reply: ExchangeReply):
        await self._redis.rpush(f"exchange_replies:{reply.exchange_id}", reply.model_dump_json())  # type: ignore
        await self._redis.expireat(f"exchange_replies:{reply.exchange_id}", exchange.expire_at)

    async def get_replies(self, exchange_id: str):
        data = await self._redis.lrange(f"exchange_replies:{exchange_id}", 0, -1)  # type: ignore
        return [ExchangeReply.model_validate_json(reply) for reply in data]

    async def delete_exchange(self, id: str):
        await self._redis.delete(f"exchange:{id}", f"exchange_replies:{id}")


_storage = MemoryStorage()

_redis_connection_pool = (
    redis.ConnectionPool.from_url(settings.redis_url) if settings.redis_url else None
)


async def get_storage():
    if _redis_connection_pool:
        yield RedisStorage(redis.Redis(connection_pool=_redis_connection_pool))
    else:
        yield _storage


async def get_exchange(
    storage: Annotated[Storage, Depends(get_storage)],
    exchange_id: Annotated[str, Path(pattern="^[0-9a-f]{16}$")],
):
    exchange = await storage.get_exchange(exchange_id)
    if exchange is None:
        raise HTTPException(status_code=404, detail="Exchange not found")

    yield exchange
