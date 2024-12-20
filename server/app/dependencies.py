import redis.asyncio as redis

from app.config import settings

_redis_connection_pool = (
    redis.ConnectionPool.from_url(settings.redis_url) if settings.redis_url else None
)
_fake_redis_server = None

if _redis_connection_pool is None:
    from fakeredis import FakeAsyncRedis, FakeServer

    _fake_redis_server = FakeServer()


async def get_redis():
    if _redis_connection_pool:
        yield redis.Redis(connection_pool=_redis_connection_pool)
    else:
        yield FakeAsyncRedis(server=_fake_redis_server)
