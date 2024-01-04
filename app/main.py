from fastapi import FastAPI, HTTPException, Depends
from fastapi_users import FastAPIUsers

from app.auth.auth import auth_backend
from app.auth.database import User
from app.auth.manager import get_user_manager
from app.auth.schemas import UserRead, UserCreate, UserUpdate

# from app.config import REDIS_URL
# from app.users.routers import router
# from app.users.models import redis_client



app = FastAPI(title="LookAround")

# app.include_router(router)
# Создание клиента Redis
# redis_client = redis.Redis.from_url(REDIS_URL)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/redis_strategy",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


current_user = fastapi_users.current_user()

@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get('/')
def hello():
    return 'Hello World'

#
# @app.get("/test_redis")
# async def test_redis():
#     try:
#         # Асинхронно записываем значение в Redis
#         await redis_client.set("test_key", "Hello Redis")
#
#         # Асинхронно читаем значение из Redis
#         value = await redis_client.get("test_key")
#
#         # Возвращаем значение
#         return {"test_key": value}
#     except redis.RedisError as e:
#         raise HTTPException(status_code=500, detail=f"Ошибка подключения к Redis: {e}")


