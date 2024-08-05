from collections import defaultdict
from typing import Annotated

from fastapi import Depends, HTTPException, Path

from app.exchanges.models import Exchange, ExchangeReply


class Storage:
    def __init__(self):
        self._exchanges = {}
        self._exchange_replies = defaultdict(list)

    async def save_exchange(self, exchange: Exchange):
        self._exchanges[exchange.id] = exchange.model_dump_json()

    async def get_exchange(self, exchange_id: str):
        exchange = self._exchanges.get(exchange_id)
        if exchange is None:
            return None
        return Exchange.model_validate_json(exchange)

    async def push_reply(self, reply: ExchangeReply):
        self._exchange_replies[reply.exchange_id].append(reply.model_dump_json())

    async def get_replies(self, exchange_id: str):
        replies = self._exchange_replies.get(exchange_id, [])
        return [ExchangeReply.model_validate_json(reply) for reply in replies]

    async def delete_exchange(self, id: str):
        if id in self._exchanges:
            del self._exchanges[id]
            del self._exchange_replies[id]


_storage = Storage()


async def get_storage():
    yield _storage


async def get_exchange(
    storage: Annotated[Storage, Depends(get_storage)],
    exchange_id: Annotated[str, Path(pattern="^[0-9a-f]{16}$")],
):
    exchange = await storage.get_exchange(exchange_id)
    if exchange is None:
        raise HTTPException(status_code=404, detail="Exchange not found")

    yield exchange
