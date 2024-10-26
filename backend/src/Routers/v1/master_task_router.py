from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.MasterTaskController import MasterTaskController
from src.Schemas.MasterTaskSchemas import MasterTaskInput, MasterTaskOutput

router = APIRouter(prefix="/api/v1/master_tasks", tags=["Master tasks"])


@router.get("/", response_model=List[MasterTaskOutput])
async def get_tasks(session: AsyncSession = Depends(get_session)):
    return await MasterTaskController.get_all(session)


@router.get("/{task_id}", response_model=MasterTaskOutput)
async def get_task(task_id: int, session: AsyncSession = Depends(get_session)):
    return await MasterTaskController.get_one(task_id, session)


@router.post("/", response_model=MasterTaskOutput)
async def create_task(task: MasterTaskInput, session: AsyncSession = Depends(get_session)):
    return await MasterTaskController.create(task, session)


@router.put("/{task_id}", response_model=MasterTaskOutput)
async def update_task(task_id: int, task_data: MasterTaskInput, session: AsyncSession = Depends(get_session)):
    return await MasterTaskController.update(task_id, task_data, session)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, session: AsyncSession = Depends(get_session)):
    return await MasterTaskController.delete(task_id, session)
