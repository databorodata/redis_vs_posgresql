from fastapi import FastAPI
from app.auth_sql.database import create_db_and_tables
from app.auth_redis.router_redis import router as redis_router
from app.auth_sql.router_sql import router as sql_router

app = FastAPI(title="LookAround")

app.include_router(redis_router, prefix="/auth/redis", tags=['REDIS'],)
app.include_router(sql_router, prefix="/auth/sql", tags=['SQL'],)


@app.on_event("startup")
async def on_startup():
    await create_db_and_tables()
