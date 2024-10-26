from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.Config.db import engine, Base
from src.Routers.v1.user_router import router as user_router
from src.Routers.v1.role_router import router as role_router
from src.Routers.v1.auth_router import router as auth_router
from src.Routers.v1.command_router import router as command_router

app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(command_router)
