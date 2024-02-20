from fastapi import Depends
from fastapi_users.authentication import AuthenticationBackend, BearerTransport
from fastapi_users.authentication.strategy import AccessTokenDatabase, DatabaseStrategy

from app.auth_sql.database import AccessToken, get_access_token_db

# bearer_transport = BearerTransport(tokenUrl="auth/redis_strategy/login")
bearer_transport = BearerTransport(tokenUrl="/auth/sql")


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


sql_auth_backend = AuthenticationBackend(
    name="sql_strategy",
    transport=bearer_transport,
    get_strategy=get_database_strategy,
)

