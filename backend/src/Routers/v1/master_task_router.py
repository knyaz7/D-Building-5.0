from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.MasterTaskController import MasterTaskController
from src.Schemas.MasterTaskSchemas import MasterTaskInput, MasterTaskOutput
from src.Schemas.TaskSchemas import TaskInput, TaskOutput

router = APIRouter(prefix="/api/v1/master_tasks", tags=["Master tasks"])


@router.get("/", response_model=List[MasterTaskOutput])
async def get_master_tasks(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session, 1)
    return await MasterTaskController.get_all(session)


@router.get("/{task_id}", response_model=MasterTaskOutput)
async def get_master_task(task_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session, 1)
    return await MasterTaskController.get_one(task_id, session)


@router.post("/", response_model=MasterTaskOutput)
async def create_master_task(task: MasterTaskInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session, 1)
    return await MasterTaskController.create(task, session)


@router.put("/{task_id}", response_model=MasterTaskOutput)
async def update_master_task(task_id: int, task_data: MasterTaskInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session, 1)
    return await MasterTaskController.update(task_id, task_data, session)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_master_task(task_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session, 1)
    return await MasterTaskController.delete(task_id, session)


@router.post("/{master_task_id}/add_task/", response_model=TaskOutput)
async def create_task(master_task_id: int, task_data: TaskInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session, 1)
    return await MasterTaskController.create_task(master_task_id, task_data, session)


@router.delete("/{master_task_id}/delete_stack/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(master_task_id: int, task_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session, 1)
    return await MasterTaskController.delete_task(master_task_id, task_id, session)
