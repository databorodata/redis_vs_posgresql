


# # import uuid
# from fastapi import HTTPException, Depends, APIRouter
# from fastapi.security import OAuth2PasswordRequestForm
# from pydantic import EmailStr
# from fastapi_users import exceptions
#
# from app.users.auth import oauth2_scheme
# # from app.users.auth import authenticate_user, get_current_user
# # from passlib.context import CryptContext
# from app.users.models import redis_strategy, user_manager, UserManager, User, user_db
#
# router = APIRouter()
#
# from fastapi import Depends, HTTPException, status
# from fastapi.security import OAuth2PasswordBearer
# from fastapi_users import models
# from app.users.models import UserManager, redis_client
#
# # pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
#
#
# async def get_user_manager():
#     return user_manager
#
# @router.post("/register")
# async def register_user(
#     email: EmailStr, password: str, name: str,
#     user_manager: UserManager = Depends(get_user_manager)
# ):
#     user_data = User(
#         email=email,
#         hashed_password=password,  # Пароль будет хешироваться в UserManager
#         name=name,
#         is_active=True,
#         is_superuser=False,
#         is_verified=False
#     )
#
#     try:
#         # Создание пользователя
#         new_user = await user_manager.create(user_data)
#         return {"message": "Пользователь создан успешно"}
#     except exceptions.UserAlreadyExists:
#         # Обработка ситуации, когда пользователь уже существует
#         raise HTTPException(status_code=400, detail="Пользователь с таким email уже существует")
#
#
# @router.post("/login")
# async def login(
#     form_data: OAuth2PasswordRequestForm = Depends(),
#     user_manager: UserManager = Depends(get_user_manager)
# ):
#     # Аутентификация пользователя
#     user = await user_manager.authenticate(credentials=form_data)
#     if not user:
#         raise HTTPException(status_code=400, detail="Некорректные учетные данные")
#
#     # Генерация токена доступа
#     token = await redis_strategy.write_token(user)
#     return {"access_token": token, "token_type": "bearer"}
#
#
# #
# #
# # @router.post("/logout")
# # async def logout(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
# #     '''
# #     oauth2_scheme в FastAPI — это экземпляр класса OAuth2PasswordBearer,
# #     который используется для получения токена доступа из запроса. Это часть механизма
# #     безопасности FastAPI, который помогает в реализации OAuth2 аутентификации с использованием JWT токенов.
# #     '''
# #     try:
# #         token_exists = await redis_client.exists(f"{redis_strategy.key_prefix}{token}")
# #         print('token_exists: ', token_exists)
# #         if not token_exists:
# #             raise HTTPException(status_code=400, detail="Токен не найден")
# #
# #         await redis_strategy.destroy_token(token, current_user)
# #         return {"message": "Вы успешно вышли из системы"}
# #     except HTTPException as http_exc:
# #         # Перенаправление HTTP исключений
# #         raise http_exc
# #     except Exception as e:
# #         # Обработка других ошибок
# #         raise HTTPException(status_code=500, detail=f"Внутренняя ошибка сервера: {e}")
#
# # @router.post("/logout")
# # async def logout(token: str = Depends(oauth2_scheme)):
# #     await redis_strategy.destroy_token(token)
# #     return {"message": "Вы вышли из системы"}
#
#
#
#
#
# # Используйте OAuth2PasswordBearer для получения токена из запроса
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
#
# async def get_current_user(token: str = Depends(oauth2_scheme), user_manager: UserManager = Depends(get_user_manager)):
#     # Попытка декодировать и проверить токен
#     user = await redis_client.get(token)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Недействительный или просроченный токен")
#     return user
#
# @router.post("/logout")
# async def logout(current_user: models.User = Depends(get_current_user)):
#     token = oauth2_scheme.credentials
#     if token:
#         # Удалить токен из Redis
#         await redis_client.delete(token)
#         return {"message": "Вы успешно вышли из системы"}
#     raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Токен не найден")
#
#
# # curl -X POST "http://0.0.0.0:8000/logout" -H "Authorization: Bearer fhuiF7h9Ce5ThXINpQPBtdSug-3u-r0Kn0U8xTe_UtM"
#
#
#
