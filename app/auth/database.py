import json
import logging
import uuid
from random import randint
from typing import Optional, Dict, Any

from fastapi_users.authentication import RedisStrategy
import redis.asyncio as redis
from fastapi_users.db import BaseUserDatabase
from pydantic import BaseModel, EmailStr

from app.config import REDIS_HOST, REDIS_PORT, REDIS_DB
# redis_client = redis.from_url("redis://localhost:6379")

REDIS_URL = f"redis://{REDIS_HOST}:{REDIS_PORT}/{REDIS_DB}"
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


class User(BaseModel):
    id: Optional[int] = None
    email: EmailStr
    hashed_password: str
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    name: str



class RedisUserDatabase(BaseUserDatabase[User, str]):
# class RedisUserDatabase:
    def __init__(self, redis_client: redis.Redis):
        self.redis = redis_client

    async def create(self, user_data: dict) -> User:
        logger.info("Создание пользователя: %s", user_data)

        user_id = randint(1, 100000) if user_data.get('id') is None else user_data['id']
        user_data['id'] = user_id

        # Создаем экземпляр пользователя
        user = User(**user_data)

        # Сериализация данных пользователя в JSON
        user_json = user.model_dump_json()
        logger.info("Сериализованные данные пользователя: %s", user_json)

        # Сохранение данных пользователя в Redis
        await self.redis.set(f"user:{user_id}", user_json)
        logger.info("Пользователь сохранен в Redis под ключом: user:%s", user_id)

        await self.redis.set(f"email_to_id:{user.email}", user_id)
        logger.info("Соответствие email и ID сохранено: email_to_id:%s -> %s", user.email, user_id)

        return user

    async def get(self, id: int) -> Optional[User]:
        user_json = await self.redis.get(f"user:{id}")
        if user_json:
            user_data = json.loads(user_json)  # Десериализация JSON-строки в словарь
            return User(**user_data)
        return None


    async def get_by_email(self, email: str) -> Optional[User]:
        logger.info(f"Поиск пользователя по email: {email}")

        user_id = await self.redis.get(f"email_to_id:{email}")
        if user_id:
            logger.info(f"Найден ID пользователя: {user_id}")

            user_json = await self.redis.get(f"user:{user_id}")
            if user_json:
                logger.info(f"Найдены данные пользователя в Redis: {user_json}")
                user = User(**json.loads(user_json))
                logger.info(f"Пользователь десериализован: {user}")
                return user
            else:
                logger.warning(f"Данные пользователя не найдены в Redis для ID: {user_id}")
        else:
            logger.warning(f"Пользователь с email {email} не найден")

        return None

    async def update(self, user: User, update_dict: Dict[str, Any]) -> User:
        user_id = str(user.id)
        logger.info(f"Обновление пользователя с ID: {user_id}")

        # Получаем текущие данные пользователя и обновляем их
        user_data = user.model_dump()
        user_data.update(update_dict)

        # Создаем обновленный экземпляр пользователя
        updated_user = User(**user_data)

        # Сериализация и сохранение обновленного пользователя в Redis
        user_json = updated_user.model_dump_json()
        await self.redis.set(f"user:{user_id}", user_json)
        logger.info(f"Пользователь с ID: {user_id} обновлен в Redis")

        return updated_user

    async def delete(self, user: User) -> None:
        user_id = str(user.id)
        logger.info(f"Удаление пользователя с ID: {user_id}")

        # Удаление пользователя из Redis
        await self.redis.delete(f"user:{user_id}")
        logger.info(f"Пользователь с ID: {user_id} удален из Redis")

        # Удаление соответствия email и ID пользователя (если необходимо)
        await self.redis.delete(f"email_to_id:{user.email}")
        logger.info(f"Соответствие email и ID для пользователя с ID: {user_id} удалено из Redis")

    async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[User]:
        user_id = await self.redis.get(f"oauth:{oauth}:{account_id}")
        if user_id:
            return await self.get(user_id)
        return None

    async def add_oauth_account(self, user: User, create_dict: Dict[str, Any]) -> User:
        # Реализуйте логику добавления информации об OAuth-аккаунте
        pass

    async def update_oauth_account(self, user: User, oauth_account, update_dict: Dict[str, Any]) -> User:
        # Реализуйте логику обновления информации об OAuth-аккаунте
        pass



async def get_user_db():
    yield RedisUserDatabase(redis_client)

