




# from fastapi.security import OAuth2PasswordBearer
# from jose import JWTError, jwt
# from datetime import datetime, timedelta
# import json
# from passlib.context import CryptContext
# from starlette import status
# from app.users.models import UserManager, user_manager, User
# from fastapi import HTTPException, Depends
# from app.users.models import redis_client, redis_strategy
# from fastapi import HTTPException, status
# from typing import Optional
#
# # Это ваш секретный ключ для создания JWT токенов.
# SECRET_KEY = "your_secret_key"
#
# # Алгоритм, который используется для создания JWT токенов.
# ALGORITHM = "HS256"
#
# # Экземпляр OAuth2PasswordBearer, который указывает, где ваш API ожидает получить токен.
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# # Контекст для хеширования и проверки паролей.
# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# # Функция для создания JWT токенов.
# # def create_access_token(data: dict):
# #     # Копируем данные пользователя.
# #     to_encode = data.copy()
# #     # Устанавливаем время истечения токена.
# #     expire = datetime.utcnow() + timedelta(minutes=15)
# #     to_encode.update({"exp": expire})
# #     # Создаем JWT токен.
# #     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
# #     return encoded_jwt
#
# #
# # async def verify_token(token: str, credentials_exception):
# #     try:
# #         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
# #         username: str = payload.get("sub")
# #         if username is None:
# #             raise credentials_exception
# #         user = await get_user_by_username(username)
# #         if user is None:
# #             raise credentials_exception
# #         return user
# #     except JWTError as e:
# #         # Более подробная информация об ошибке
# #         print(f"Ошибка при декодировании JWT: {e}")
# #         raise HTTPException(
# #             status_code=status.HTTP_401_UNAUTHORIZED,
# #             detail=f"Ошибка JWT: {e}"
# #         )
# #     except Exception as e:
# #         # Общий блок для перехвата других исключений
# #         print(f"Неожиданная ошибка: {e}")
# #         raise HTTPException(
# #             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
# #             detail="Внутренняя ошибка сервера"
# #         )
#
#
# async def verify_token(token: str, credentials_exception) -> Optional[User]:
#     try:
#         # Используем RedisStrategy для чтения токена
#         user = await redis_strategy.read_token(token, user_manager)
#         if user is None:
#             raise credentials_exception
#         return user
#     except Exception as e:
#         # Логирование для диагностики
#         print(f"Ошибка при проверке токена: {e}")
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Не удалось валидировать учетные данные"
#         )
#
#
# # Функция для проверки пароля.
# async def verify_password(plain_password, hashed_password):
#     # Сравниваем переданный пароль и хешированный пароль.
#     return pwd_context.verify(plain_password, hashed_password)
#
#
# # Асинхронная функция для аутентификации пользователя.
# async def authenticate_user(username: str, password: str) -> User:
#     print('authenticate_user, username: ', username)
#     # Получаем пользователя по имени пользователя.
#     user = await get_user_by_username(username)
#     print('authenticate_user: ', user.__dict__)
#     # Если пользователь не найден, выкидываем исключение.
#     if user is None:
#         raise HTTPException(status_code=404, detail="Пользователь не найден")
#     # Проверяем пароль.
#     if not await verify_password(password, user.hashed_password):
#         # Если пароль неверный, выкидываем исключение.
#         raise HTTPException(status_code=401, detail="Неправильный пароль")
#     return user
#
#
# # # Асинхронная функция для получения пользователя по имени из Redis.
# # async def get_user_by_username(username: str) -> User:
# #     # Получаем данные пользователя из Redis.
# #     # user_data = await redis_client.get(f"user:{username}")
# #     print('get_user_by_username', 'username: ', username)
# #     print(redis_client)
# #     user_data = await redis_client.get(f"user:{username}")
# #     if user_data:
# #         # Если данные найдены, десериализуем их и возвращаем объект пользователя.
# #         user_dict = json.loads(user_data)
# #         return User(**user_dict)
# #     else:
# #         # Если пользователь не найден, выкидываем исключение.
# #         raise HTTPException(status_code=404, detail="Пользователь не найден")
#
#
# async def get_user_by_username(username: str) -> User:
#     try:
#         user_data = await redis_client.get(f"user:{username}")
#         if user_data:
#             user_dict = json.loads(user_data)
#             return User(**user_dict)
#         else:
#             raise HTTPException(status_code=404, detail="Пользователь не найден")
#     except Exception as e:
#         # Обработка ошибок связанных с Redis
#         raise HTTPException(status_code=500, detail=f"Ошибка Redis: {e}")
#
#
# # Асинхронная функция для получения текущего пользователя по токену.
# async def get_current_user(token: str = Depends(oauth2_scheme)):
#     # Создаем исключение для случая, если токен невалиден.
#     print('get_current_user: ', token)
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Не удалось валидировать учетные данные",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     x = await verify_token(token, credentials_exception)
#     print('x', await verify_token(token, credentials_exception))
#     return x
#
# # async def get_current_user(token: str = Depends(oauth2_scheme)):
# #     user_id = await redis_strategy.read_token(token)
# #     if user_id is None:
# #         raise HTTPException(status_code=401, detail="Неавторизован")
# #     # Получение объекта пользователя...
#
