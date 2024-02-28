from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from app.auth_sql.auth import sql_auth_backend
from app.auth_sql.database import User
from app.auth_sql.manager import get_sql_user_manager
from app.auth_sql.schemas import UserRead, UserCreate

router = APIRouter()

fastapi_users_sql = FastAPIUsers[User, int](
    get_sql_user_manager,
    [sql_auth_backend],
)

router.include_router(fastapi_users_sql.get_register_router(UserRead, UserCreate))


router.include_router(fastapi_users_sql.get_auth_router(sql_auth_backend))


router.include_router(fastapi_users_sql.get_auth_router(sql_auth_backend),)
