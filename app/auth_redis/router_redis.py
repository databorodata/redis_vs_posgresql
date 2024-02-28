from fastapi import APIRouter
from app.auth_redis.auth import redis_auth_backend
from app.auth_redis.manager import get_redis_user_manager
from app.auth_sql.schemas import UserRead, UserCreate
from fastapi_users import FastAPIUsers
from app.auth_sql.database import User

router = APIRouter()

fastapi_users_redis = FastAPIUsers[User, int](
    get_redis_user_manager,
    [redis_auth_backend],
)


router.include_router(
    fastapi_users_redis.get_register_router(UserRead, UserCreate))


router.include_router(
    fastapi_users_redis.get_auth_router(redis_auth_backend))


router.include_router(fastapi_users_redis.get_reset_password_router())
