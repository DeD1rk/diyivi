from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, HTTPException, Path

from app.dependencies import get_redis
from app.exchanges.models import Exchange, ExchangeReply


class ExchangesStorage:
    """Storage backend using Redis.

    This stores `Exchange` objects as JSON strings at `exchange:{id}`.
    The corresponding replies are stored in a list at `exchange_replies:{id}`,
    in order of creation.
    """

    def __init__(self, redis: redis.Redis):
        self._redis = redis

    async def save_exchange(self, exchange: Exchange) -> None:
        """Save or update an exchange."""
        await self._redis.set(
            f"exchange:{exchange.id}",
            exchange.model_dump_json(),
            exat=exchange.expire_at,
        )

    async def get_exchange(self, id: str) -> Exchange | None:
        """Get an exchange by its ID, or None if it doesn't exist."""
        data = await self._redis.get(f"exchange:{id}")
        return Exchange.model_validate_json(data) if data else None

    async def push_reply(self, exchange: Exchange, reply: ExchangeReply) -> None:
        """Add a new reply to an exchange."""
        await self._redis.rpush(f"exchange_replies:{reply.exchange_id}", reply.model_dump_json())  # type: ignore
        await self._redis.expireat(f"exchange_replies:{reply.exchange_id}", exchange.expire_at)

    async def get_replies(self, exchange_id: str) -> list[ExchangeReply]:
        """Get all replies for an exchange.

        Returns an empty list if the exchange doesn't exist.
        """
        data = await self._redis.lrange(f"exchange_replies:{exchange_id}", 0, -1)  # type: ignore
        return [ExchangeReply.model_validate_json(reply) for reply in data]

    async def delete_exchange(self, id: str) -> None:
        """Delete an exchange and any replies by its ID."""
        await self._redis.delete(f"exchange:{id}", f"exchange_replies:{id}")


async def get_exchanges_storage(redis: Annotated[redis.Redis, Depends(get_redis)]):
    yield ExchangesStorage(redis)


async def get_exchange(
    storage: Annotated[ExchangesStorage, Depends(get_exchanges_storage)],
    exchange_id: Annotated[str, Path(pattern="^[0-9a-f]{16}$")],
):
    exchange = await storage.get_exchange(exchange_id)
    if exchange is None:
        raise HTTPException(status_code=404, detail="Exchange not found")

    yield exchange
