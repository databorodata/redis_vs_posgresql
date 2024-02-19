from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi_users import FastAPIUsers
from app.auth.auth import auth_backend
from app_sql.database import User, create_db_and_tables
from app.auth.manager import get_user_manager
from app_sql.schemas import UserRead, UserCreate, UserUpdate


app = FastAPI(title="LookAround")


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/redis_strategy",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)


app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"],
)


current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.email}"


@app.get('/')
def hello():
    return 'Hello World'

