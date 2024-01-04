




# import uuid
# from fastapi_users.db import BaseUserDatabase
# from pydantic import BaseModel, EmailStr, json
# from typing import Dict, Any
# import redis.asyncio as redis
# from fastapi_users.authentication import RedisStrategy
# import logging
# import json
# from fastapi import Request, Response
# from fastapi_users.manager import BaseUserManager
# from typing import Optional, TypeVar
# from fastapi_users import exceptions
#
# import uuid
# from typing import Any, Dict, Generic, Optional, Union
#
# import jwt
# from fastapi.security import OAuth2PasswordRequestForm
#
# from fastapi_users import exceptions, models, schemas
# from fastapi_users.db import BaseUserDatabase
# from fastapi_users.jwt import SecretType, decode_jwt, generate_jwt
# from fastapi_users.password import PasswordHelper, PasswordHelperProtocol
# from fastapi_users.types import DependencyCallable
#
# RESET_PASSWORD_TOKEN_AUDIENCE = "fastapi-users:reset"
# VERIFY_USER_TOKEN_AUDIENCE = "fastapi-users:verify"
#
# logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.INFO)
#
# ID = TypeVar("ID")
# redis_client = redis.from_url("redis://localhost:6379")
#
#
# class User(BaseModel):
#     id: Optional[str] = None
#     email: EmailStr
#     hashed_password: str
#     is_active: bool = True
#     is_superuser: bool = False
#     is_verified: bool = False
#     name: str
#
#
# class RedisUserDatabase(BaseUserDatabase[User, str]):
# # class RedisUserDatabase:
#     def __init__(self, redis_client: redis.Redis):
#         self.redis = redis_client
#
#     async def create(self, user_data: dict) -> User:
#         logger.info("Создание пользователя: %s", user_data)
#
#         user_id = str(uuid.uuid4()) if user_data.get('id') is None else user_data['id']
#         user_data['id'] = user_id
#
#         # Создаем экземпляр пользователя
#         user = User(**user_data)
#
#         # Сериализация данных пользователя в JSON
#         user_json = user.model_dump_json()
#         logger.info("Сериализованные данные пользователя: %s", user_json)
#
#         # Сохранение данных пользователя в Redis
#         await self.redis.set(f"user:{user_id}", user_json)
#         logger.info("Пользователь сохранен в Redis под ключом: user:%s", user_id)
#
#         await self.redis.set(f"email_to_id:{user.email}", user_id)
#         logger.info("Соответствие email и ID сохранено: email_to_id:%s -> %s", user.email, user_id)
#
#         return user
#
#     async def get(self, id: str) -> Optional[User]:
#         user_json = await self.redis.get(f"user:{id}")
#         if user_json:
#             user_data = json.loads(user_json)  # Десериализация JSON-строки в словарь
#             return User(**user_data)
#         return None
#
#
#     async def get_by_email(self, email: str) -> Optional[User]:
#         logger.info(f"Поиск пользователя по email: {email}")
#
#         user_id = await self.redis.get(f"email_to_id:{email}")
#         if user_id:
#             user_id = user_id.decode("utf-8")
#             logger.info(f"Найден ID пользователя: {user_id}")
#
#             user_json = await self.redis.get(f"user:{user_id}")
#             if user_json:
#                 logger.info(f"Найдены данные пользователя в Redis: {user_json}")
#                 user = User(**json.loads(user_json))
#                 logger.info(f"Пользователь десериализован: {user}")
#                 return user
#             else:
#                 logger.warning(f"Данные пользователя не найдены в Redis для ID: {user_id}")
#         else:
#             logger.warning(f"Пользователь с email {email} не найден")
#
#         return None
#
#     async def update(self, user: User, update_dict: Dict[str, Any]) -> User:
#         user_id = str(user.id)
#         logger.info(f"Обновление пользователя с ID: {user_id}")
#
#         # Получаем текущие данные пользователя и обновляем их
#         user_data = user.model_dump()
#         user_data.update(update_dict)
#
#         # Создаем обновленный экземпляр пользователя
#         updated_user = User(**user_data)
#
#         # Сериализация и сохранение обновленного пользователя в Redis
#         user_json = updated_user.model_dump_json()
#         await self.redis.set(f"user:{user_id}", user_json)
#         logger.info(f"Пользователь с ID: {user_id} обновлен в Redis")
#
#         return updated_user
#
#     async def delete(self, user: User) -> None:
#         user_id = str(user.id)
#         logger.info(f"Удаление пользователя с ID: {user_id}")
#
#         # Удаление пользователя из Redis
#         await self.redis.delete(f"user:{user_id}")
#         logger.info(f"Пользователь с ID: {user_id} удален из Redis")
#
#         # Удаление соответствия email и ID пользователя (если необходимо)
#         await self.redis.delete(f"email_to_id:{user.email}")
#         logger.info(f"Соответствие email и ID для пользователя с ID: {user_id} удалено из Redis")
#
#     async def get_by_oauth_account(self, oauth: str, account_id: str) -> Optional[User]:
#         user_id = await self.redis.get(f"oauth:{oauth}:{account_id}")
#         if user_id:
#             return await self.get(user_id)
#         return None
#
#     async def add_oauth_account(self, user: User, create_dict: Dict[str, Any]) -> User:
#         # Реализуйте логику добавления информации об OAuth-аккаунте
#         pass
#
#     async def update_oauth_account(self, user: User, oauth_account, update_dict: Dict[str, Any]) -> User:
#         # Реализуйте логику обновления информации об OAuth-аккаунте
#         pass
#
#
# user_db = RedisUserDatabase(redis_client)
#
#
# class UserManager(BaseUserManager[User, str]):
#     user_db_model = User
#
#     def __init__(self, user_db: RedisUserDatabase):
#         super().__init__(user_db)
#
#     async def create(
#         self,
#         user: User,  # Изменено с user_create: schemas.UC
#         safe: bool = False,
#         request: Optional[Request] = None,
#     ) -> User:
#         # Проверяем, существует ли пользователь с таким же email
#         if await self.user_db.get_by_email(user.email) is not None:
#             raise exceptions.UserAlreadyExists()
#
#         # Валидация пароля
#         # await self.validate_password(user.hashed_password, user)
#
#         # Хеширование пароля
#         user.hashed_password = self.password_helper.hash(user.hashed_password)
#
#         # Создание пользователя
#         created_user = await self.user_db.create(user.model_dump())  # Используем .dict() для получения данных из модели Pydantic
#
#         # Вызываем хук после регистрации
#         await self.on_after_register(created_user, request)
#
#         return created_user
#
#     async def get_by_email(self, user_email: str) -> User:
#         """
#         Get a user by e-mail.
#
#         :param user_email: E-mail of the user to retrieve.
#         :return: A user if exists, otherwise None.
#         """
#         user = await self.user_db.get_by_email(user_email)
#         return user
#
#     # Здесь вы можете переопределить или добавить любые методы, если это необходимо.
#     # Например, для кастомной логики после регистрации пользователя или сброса пароля.
#
#     async def on_after_register(self, user: User, request: Optional[Request] = None):
#         # Кастомная логика после регистрации пользователя
#         pass
#
#     async def on_after_forgot_password(self, user: User, token: str, request: Optional[Request] = None):
#         # Кастомная логика после запроса на сброс пароля
#         pass
#
#
# user_manager = UserManager(user_db)
# redis_strategy = RedisStrategy(redis_client, lifetime_seconds=3600)
#
#
#
#
#
