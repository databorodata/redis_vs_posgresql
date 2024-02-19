from fastapi import FastAPI, Depends
from fastapi_users import FastAPIUsers
from app.auth_redis.auth import redis_auth_backend
from app.auth_sql.auth import sql_auth_backend
from app.auth_sql.database import User, create_db_and_tables
from app.auth_redis.manager import get_redis_user_manager
from app.auth_sql.manager import get_sql_user_manager
from app.auth_sql.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI(title="LookAround")


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

fastapi_users_redis = FastAPIUsers[User, int](
    get_redis_user_manager,
    [redis_auth_backend],
)


app.include_router(
    fastapi_users_redis.get_auth_router(redis_auth_backend),
    prefix="/auth/redis_strategy",
    tags=["auth:redis"],
)


app.include_router(
    fastapi_users_redis.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth:redis"],
)


app.include_router(
    fastapi_users_redis.get_reset_password_router(),
    prefix="/auth",
    tags=["auth:redis"],
)


app.include_router(
    fastapi_users_redis.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth:redis"],
)


app.include_router(
    fastapi_users_redis.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users:redis"],
)





fastapi_users_sql = FastAPIUsers[User, int](
    get_sql_user_manager,
    [sql_auth_backend],
)


app.include_router(
    fastapi_users_sql.get_auth_router(sql_auth_backend),
    prefix="/auth/sql_strategy",
    tags=["auth:sql"],
)

app.include_router(
    fastapi_users_sql.get_register_router(UserRead, UserCreate),
    prefix="/auth/sql_strategy",
    tags=["auth:sql"],
)

app.include_router(
    fastapi_users_sql.get_reset_password_router(),
    prefix="/auth/sql_strategy",
    tags=["auth:sql"],
)

app.include_router(
    fastapi_users_sql.get_verify_router(UserRead),
    prefix="/auth/sql_strategy",
    tags=["auth:sql"],
)

app.include_router(
    fastapi_users_sql.get_users_router(UserRead, UserUpdate),
    prefix="/users/sql_strategy",
    tags=["users:sql"],
)


current_user_redis = fastapi_users_redis.current_user()
current_user_sql = fastapi_users_sql.current_user()


@app.get("/redis/protected-route")
def protected_route_redis(user: User = Depends(current_user_redis)):
    return f"Hello, {user.email} from Redis"


@app.get("/sql/protected-route")
def protected_route_sql(user: User = Depends(current_user_sql)):
    return f"Hello, {user.email} from SQL"


@app.get('/')
def hello():
    return 'Hello World'





