from sqlalchemy import Column, Integer, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from src.Config.db import Base


class MasterTask(Base):
    __tablename__ = 'master_tasks'

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, nullable=False)
    deadline = Column(DateTime, nullable=False)
    tasks = Column(ARRAY(Integer), nullable=False)
