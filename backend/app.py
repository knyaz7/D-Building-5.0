from fastapi import FastAPI

from src.Config.db import engine, Base
from src.Routers.v1.user_router import router as user_router
from src.Routers.v1.role_router import router as role_router
from src.Routers.v1.auth_router import router as auth_router
from src.Routers.v1.task_router import router as task_router
from src.Routers.v1.master_task_router import router as master_task_router
from src.Routers.v1.point_router import router as point_router
from src.Routers.v1.tool_router import router as tool_router
from src.Routers.v1.position_router import router as position_router
from src.Routers.v1.comment_router import router as comment_router
from src.Routers.v1.user_meta_router import router as user_meta_router
from src.Routers.v1.stage_router import router as stage_router
#from src.Routers.v1.command_router import router as command_router

from src.Helpers.MiddlewareHelper import MiddlewareHelper
from src.Helpers.SeederHelper import SeederHelper

app = FastAPI()

MiddlewareHelper.setCors(app)

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await SeederHelper.run_seeder()

app.include_router(role_router)
app.include_router(user_router)
app.include_router(auth_router)
app.include_router(task_router)
app.include_router(master_task_router)
app.include_router(point_router)
app.include_router(tool_router)
app.include_router(position_router)
app.include_router(comment_router)
app.include_router(user_meta_router)
app.include_router(stage_router)
#app.include_router(command_router)
