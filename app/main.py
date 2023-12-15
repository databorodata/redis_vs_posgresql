from fastapi import FastAPI, HTTPException, Depends
from app.config import REDIS_URL
from app.users.routers import router

import redis.asyncio as redis


app = FastAPI()
app.include_router(router)
# Создание клиента Redis
# redis_client = redis.Redis.from_url(REDIS_URL)

redis_client = redis.from_url("redis://localhost:6379")


from app.users.auth import create_access_token, verify_token, oauth2_scheme
from fastapi.security import OAuth2PasswordRequestForm




@app.get('/')
def hello():
    return 'Hello World'


@app.get("/test_redis")
def test_redis():
    try:
        # Записываем значение в Redis
        redis_client.set("test_key", "Hello Redis")

        # Читаем значение из Redis
        value = redis_client.get("test_key")

        # Возвращаем значение
        return {"test_key": value.decode("utf-8")}
    except redis.RedisError:
        raise HTTPException(status_code=500, detail="Ошибка подключения к Redis")

