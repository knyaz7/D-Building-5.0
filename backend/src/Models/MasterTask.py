from sqlalchemy import Column, Integer, DateTime, ARRAY, String
from sqlalchemy.sql import functions as sqlalchemy_functions
from src.Config.db import Base


class MasterTask(Base):
    __tablename__ = 'master_tasks'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    created_at = (Column
                  (DateTime(timezone=True),
                   nullable=False,
                   server_default=sqlalchemy_functions.now())
                  )
    deadline = Column(DateTime(timezone=True), nullable=False)
    tasks = Column(ARRAY(Integer), default=list)
