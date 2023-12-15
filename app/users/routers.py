from fastapi_users.authentication import RedisStrategy
from fastapi import HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from app.users.auth import oauth2_scheme
from app.main import app
from app.users.auth import authenticate_user, get_current_user
from passlib.context import CryptContext
from app.users.models import User  # Импортируйте вашу модель пользователя
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
redis_strategy = RedisStrategy(redis_client, lifetime_seconds=3600)

router = APIRouter()

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/register")
async def register_user(username: str, email: str, password: str):
    # Проверяем, существует ли уже пользователь с таким именем или почтой
    existing_user = redis_client.get(f"user:{username}")
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь уже существует")

    # Хешируем пароль
    hashed_password = pwd_context.hash(password)

    # Создаем нового пользователя
    user = User(username=username, email=email, hashed_password=hashed_password)

    # Сохраняем пользователя в Redis
    user_data = json.dumps(user.dict())
    await redis_client.set(f"user:{username}", user_data)

    return {"message": "Пользователь создан успешно"}


@app.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):

    '''
    form_data: OAuth2PasswordRequestForm = Depends() в FastAPI это способ получения данных,
    отправленных пользователем через HTML форму. Поясню подробнее: OAuth2PasswordRequestForm: Это класс,
    предоставляемый FastAPI, который предназначен для работы с OAuth2 и формами, где пользователь отправляет
    имя пользователя (или почту) и пароль. Depends(): Это функция зависимостей в FastAPI. Она используется для
    внедрения зависимостей в пути (эндпоинты). В данном контексте она говорит FastAPI, что для обработки этого
    запроса необходимо получить данные из формы, отправленной пользователем.
    '''

    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Некорректные учетные данные")

    token = await redis_strategy.write_token(user)
    '''
    Внутри write_token, генерируется уникальный токен (с использованием secrets.token_urlsafe()).
    Этот токен затем сохраняется в Redis с помощью команды set, причем в качестве ключа используется сочетание префикса 
    (key_prefix из RedisStrategy) и самого токена. В качестве значения сохраняется ID пользователя.
    Время жизни токена (lifetime_seconds) устанавливается как время истечения ключа в Redis.
    Таким образом, когда метод write_token вызывается, он не только создает токен, 
    но и сохраняет его в Redis, связывая токен с ID пользователя.
    '''

    return {"access_token": token, "token_type": "bearer"}

@app.post("/logout")
async def logout(current_user: User = Depends(get_current_user), token: str = Depends(oauth2_scheme)):
    '''
    oauth2_scheme в FastAPI — это экземпляр класса OAuth2PasswordBearer,
    который используется для получения токена доступа из запроса. Это часть механизма
    безопасности FastAPI, который помогает в реализации OAuth2 аутентификации с использованием JWT токенов.
    '''
    await redis_strategy.destroy_token(token, current_user)
    return {"message": "Вы успешно вышли из системы"}


