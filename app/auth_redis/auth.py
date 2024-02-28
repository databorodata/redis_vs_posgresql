from fastapi_users.authentication import CookieTransport, RedisStrategy, AuthenticationBackend, BearerTransport

from app.auth_redis.database import redis_client

cookie_transport = CookieTransport(cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="/auth/redis")


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis_client, lifetime_seconds=3600)


SECRET = "SECRET"


redis_auth_backend = AuthenticationBackend(
    name="redis_strategy",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)