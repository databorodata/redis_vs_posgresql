from random import randint
from typing import Optional

import redis.asyncio as redis
from fastapi_users.db import BaseUserDatabase
from pydantic import BaseModel, EmailStr

from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB

import orjson

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    name: str

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson.dumps


class RedisUserDatabase(BaseUserDatabase[User, str]):
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def create(self, user_data: dict) -> User:
        user_id = randint(1, 100000) if user_data.get('id') is None else user_data['id']
        user_data['id'] = user_id

        user = User(**user_data)
        user_json = user.json()

        await self.redis.set(f"user:{user_id}", user_json)
        return user

    async def get(self, id: int) -> Optional[User]:
        user_json = await self.redis.get(f"user:{id}")
        if user_json:
            return User.parse_raw(user_json)
        return None


async def get_user_db():
    yield RedisUserDatabase(redis_client)
