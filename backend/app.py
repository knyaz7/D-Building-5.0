from fastapi import FastAPI

from src.Config.db import engine, Base
from src.Models.User import User
from src.Routers.v1.user_router import router as user_router
from src.Routers.v1.role_router import router as role_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(role_router)
app.include_router(user_router)
