from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey, func, select
from sqlalchemy.orm import relationship
from src.Config.db import Base


from sqlalchemy import func

class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    stack = Column(ARRAY(Integer), default=list)
    position = Column(Integer, nullable=False)
    points = Column(ARRAY(Integer), default=list)
    comments = Column(ARRAY(Integer), default=list)

    @classmethod
    async def create(cls, session, **kwargs):
        result = await session.execute(select(func.max(cls.position)))
        max_position = result.scalar() or 0
        new_task = cls(position=max_position + 1, **kwargs)
        session.add(new_task)
        await session.commit()
        return new_task
