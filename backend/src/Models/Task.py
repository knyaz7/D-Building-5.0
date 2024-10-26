from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from src.Config.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    stack = Column(ARRAY(Integer), default=list)
    position = Column(Integer, nullable=False)
    points = Column(ARRAY(Integer), default=list)
    comments = Column(ARRAY(Integer), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))
