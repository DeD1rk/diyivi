from typing import Annotated

import redis.asyncio as redis
from fastapi import Depends, HTTPException, Path

from app.dependencies import get_redis
from app.signatures.models import SignatureRequest


class SignaturesStorage:
    def __init__(self, redis: redis.Redis):
        self._redis = redis

    async def save_request(self, request: SignatureRequest) -> None:
        """Save or update a signature request."""
        await self._redis.set(
            f"signature_request:{request.id}",
            request.model_dump_json(),
            exat=request.expire_at,
        )

    async def get_request(self, id: str) -> SignatureRequest | None:
        """Get a signature request by its ID, or None if it doesn't exist."""
        data = await self._redis.get(f"signature_request:{id}")
        return SignatureRequest.model_validate_json(data) if data else None

    async def delete_request(self, id: str) -> None:
        """Delete a signature request and by its ID."""
        await self._redis.delete(f"signature_request:{id}")


async def get_signatures_storage(redis: Annotated[redis.Redis, Depends(get_redis)]):
    yield SignaturesStorage(redis)


async def get_signature_request(
    storage: Annotated[SignaturesStorage, Depends(get_signatures_storage)],
    request_id: Annotated[str, Path(pattern="^[0-9a-f]{16}$")],
):
    request = await storage.get_request(request_id)
    if request is None:
        raise HTTPException(status_code=404, detail="Signature request not found")

    yield request
