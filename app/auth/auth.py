from fastapi_users.authentication import CookieTransport, RedisStrategy, AuthenticationBackend, JWTStrategy, BearerTransport

from app.auth.database import redis_client

cookie_transport = CookieTransport(cookie_max_age=3600)
bearer_transport = BearerTransport(tokenUrl="auth/redis_strategy/login")


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis_client, lifetime_seconds=3600)


SECRET = "SECRET"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="redis_strategy",
    transport=bearer_transport,
    get_strategy=get_redis_strategy,
)