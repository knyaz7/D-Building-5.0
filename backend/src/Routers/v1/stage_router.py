from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.StageController import StageController
from src.Schemas.StageSchemas import StageInput, StageOutput
from src.Schemas.TaskSchemas import TaskInput, TaskOutput

router = APIRouter(prefix="/api/v1/stages", tags=["Stages"])


@router.get("/", response_model=List[StageOutput])
async def get_stages(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await StageController.get_all(session)


@router.get("/{stage_id}", response_model=StageOutput)
async def get_stage(stage_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await StageController.get_one(stage_id, session)


# @router.post("/", response_model=StageOutput)
# async def create_stage(tool_id: StageInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
#     await AuthController.verify_token(token, session)
#     return await StageController.create(tool_id, session)


# @router.put("/{stage_id}", response_model=StageOutput)
# async def update_stage(stage_id: int, task_data: StageInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
#     await AuthController.verify_token(token, session)
#     return await StageController.update(stage_id, task_data, session)


@router.post("/{stage_id}/add_task/", response_model=TaskOutput)
async def create_task(stage_id: int, task_data: TaskInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await StageController.create_task(stage_id, task_data, session)


@router.delete("/{stage_id}/delete_stack/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(stage_id: int, task_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await StageController.delete_task(stage_id, task_id, session)
