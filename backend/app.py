from fastapi import FastAPI

from Config.db import engine, Base
from Models.User import User
from Routers.v1.user_router import router as user_router

app = FastAPI()


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(user_router)