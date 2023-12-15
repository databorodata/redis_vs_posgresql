from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import redis
import json
from passlib.context import CryptContext
from starlette import status
from app.users.models import User
from fastapi import HTTPException, Depends

# Это ваш секретный ключ для создания JWT токенов.
SECRET_KEY = "your_secret_key"

# Алгоритм, который используется для создания JWT токенов.
ALGORITHM = "HS256"

# Экземпляр OAuth2PasswordBearer, который указывает, где ваш API ожидает получить токен.
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Контекст для хеширования и проверки паролей.
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


# Функция для создания JWT токенов.
def create_access_token(data: dict):
    # Копируем данные пользователя.
    to_encode = data.copy()
    # Устанавливаем время истечения токена.
    expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    # Создаем JWT токен.
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# Асинхронная функция для верификации JWT токенов.
async def verify_token(token: str, credentials_exception):
    try:
        # Декодируем токен.
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Извлекаем имя пользователя из токена.
        username: str = payload.get("sub")
        # Если имя пользователя не найдено, выкидываем исключение.
        if username is None:
            raise credentials_exception
        # Получаем пользователя из Redis.
        user = await get_user_by_username(username)
        # Если пользователь не найден, выкидываем исключение.
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        # Если ошибка при декодировании токена, выкидываем исключение.
        raise credentials_exception


# Функция для проверки пароля.
def verify_password(plain_password, hashed_password):
    # Сравниваем переданный пароль и хешированный пароль.
    return pwd_context.verify(plain_password, hashed_password)


# Асинхронная функция для аутентификации пользователя.
async def authenticate_user(username: str, password: str):
    # Получаем пользователя по имени пользователя.
    user = await get_user_by_username(username)
    # Если пользователь не найден, выкидываем исключение.
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    # Проверяем пароль.
    if not verify_password(password, user.hashed_password):
        # Если пароль неверный, выкидываем исключение.
        raise HTTPException(status_code=401, detail="Неправильный пароль")
    return user


# Настройка клиента Redis для работы с базой данных.
redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)


# Асинхронная функция для получения пользователя по имени из Redis.
async def get_user_by_username(username: str) -> User:
    # Получаем данные пользователя из Redis.
    user_data = await redis_client.get(f"user:{username}")
    if user_data:
        # Если данные найдены, десериализуем их и возвращаем объект пользователя.
        user_dict = json.loads(user_data)
        return User(**user_dict)
    else:
        # Если пользователь не найден, выкидываем исключение.
        raise HTTPException(status_code=404, detail="Пользователь не найден")


# Асинхронная функция для получения текущего пользователя по токену.
async def get_current_user(token: str = Depends(oauth2_scheme)):
    # Создаем исключение для случая, если токен невалиден.
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось валидировать учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_token(token, credentials_exception)


