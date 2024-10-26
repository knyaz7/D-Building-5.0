from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Controllers.TaskController import TaskController
from src.Schemas.CommentSchemas import CommentInput, CommentOutput
from src.Schemas.PointSchemas import PointInput, PointOutput
from src.Schemas.TaskSchemas import TaskInput, TaskOutput, TaskUpdate
from src.Schemas.ToolSchemas import ToolOutput

router = APIRouter(prefix="/api/v1/tasks", tags=["Tasks"])


@router.get("/", response_model=List[TaskOutput])
async def get_tasks(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await TaskController.get_all(session)


@router.get("/{task_id}", response_model=TaskOutput)
async def get_task(task_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await TaskController.get_one(task_id, session)


# @router.post("/", response_model=TaskOutput)
# async def create_task(task: TaskInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
#     await AuthController.verify_token(token, session)
#     return await TaskController.create(task, session)


@router.put("/{task_id}", response_model=TaskOutput)
async def update_task(task_id: int, task_data: TaskUpdate, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await TaskController.update(task_id, task_data, session)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(task_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    return await TaskController.delete(task_id, session)


@router.post("/{task_id}/add_comment/", response_model=CommentOutput)
async def create_task(task_id: int, comment_data: CommentInput, session: AsyncSession = Depends(get_session)):
    return await TaskController.create_comment(task_id, comment_data, session)


@router.post("/{task_id}/add_point/", response_model=PointOutput)
async def create_task(task_id: int, point_data: PointInput, session: AsyncSession = Depends(get_session)):
    return await TaskController.create_point(task_id, point_data, session)


@router.post("/{task_id}/append_tool/", response_model=ToolOutput)
async def create_task(task_id: int, tool_id: int, session: AsyncSession = Depends(get_session)):
    return await TaskController.add_tool(task_id, tool_id, session)
