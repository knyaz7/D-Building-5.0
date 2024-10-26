from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# когда teamlead создаёт master task
from src.ml.rec_employees import evaluate_employees

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Schemas.UserSchemas import UserOutput
from src.Models.User import User
from src.Models.Task import Task
from src.Models.Tool import Tool

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])

@router.get("/{task_id}", response_model=List[UserOutput])
async def get_users(task_id: int, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    query = await session.execute(select(User))
    users = query.scalars().all()
    query = await session.execute(select(Task).where(Task.id == task_id))
    task = query.scalar_one()
    query = await session.execute(select(Tool).where(Tool.id.in_(Task.stack)))
    stack = query.scalars().all()
    stack = [tool.name for tool in stack]

    return await evaluate_employees(users, task.title, stack)
