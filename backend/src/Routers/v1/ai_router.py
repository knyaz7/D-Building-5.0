from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

# когда teamlead создаёт master task
from src.ml.rec_employees import evaluate_employees

from src.Config.db import get_session
from src.Controllers.AuthController import AuthController, oauth2_scheme
from src.Schemas.UserSchemas import UserOutput
from src.Schemas.AiSchemas import AiInput
from src.Models.User import User
from src.Models.MasterTask import MasterTask
from src.Models.Tool import Tool

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])

@router.get("/{master_task_id}", response_model=List[UserOutput])
async def get_rec_users(master_task_id: int, ai_data: AiInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    query = await session.execute(select(User))
    users = query.scalars().all()
    query = await session.execute(select(MasterTask).where(MasterTask.id == master_task_id))
    master_task = query.scalar_one()
    query = await session.execute(select(Tool).where(Tool.id.in_(ai_data.stack)))
    stack = query.scalars().all()
    stack = [tool.name for tool in stack]

    return await evaluate_employees(users, master_task.name, stack)
