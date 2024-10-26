from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from src.Config.db import get_session
from src.Models.MasterTask import MasterTask
from src.Models.User import User

from src.ml.tg import create_chat_and_send_message

class WatchdogHelper:
    __threshold_percent = 0.15
    
    @staticmethod
    async def check_deadlines(session: AsyncSession = Depends(get_session)):
        query = await session.execute(select(MasterTask))
        master_tasks = query.scalars().all()
        current_date = datetime.now()

        for mt in master_tasks:
            threshold = (mt.deadline - mt.created_at).days * WatchdogHelper.__threshold_percent
            date_diff = mt.deadline - current_date
            if date_diff <= threshold:
                for task in mt.tasks:
                    query = await session.execute(select(User).where(User.id == task.user_id))
                    user = query.scalar_one()
                    create_chat_and_send_message(user.username, task, date_diff)
