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

from src.Models.UserMeta import UserMeta
from src.Models.User import User
from src.Models.MasterTask import MasterTask
from src.Models.Position import Position

router = APIRouter(prefix="/api/v1/ai", tags=["ai"])

@router.get("/{master_task_id}", response_model=List[UserOutput])
async def get_rec_users(master_task_id: int, ai_data: AiInput, token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_session)):
    await AuthController.verify_token(token, session)
    query = await session.execute(select(User))
    users = query.scalars().all()
    user_ids = [u.id for u in users]
    indexed_users = {id:item for id, item in zip(user_ids, users)}

    query = await session.execute(select(UserMeta).where(UserMeta.id.in_(user_ids)))
    users_meta = query.scalars().all()

    dict_users = []
    for um in users_meta:
        query = await session.execute(select(Position).where(Position.id == um.position_id))
        position = query.scalar_one()

        dict_users.append({
            'fullname':indexed_users[um.user_id].fullname,
            'position':position,
            'description':um.description,
            'stack':um.stack,
            'rating':um.rating
        })

    query = await session.execute(select(MasterTask).where(MasterTask.id == master_task_id))
    master_task = query.scalar_one()

    return await evaluate_employees(dict_users, master_task.name, ai_data.stack)
