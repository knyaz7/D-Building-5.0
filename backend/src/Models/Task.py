from sqlalchemy import Column, Integer, String, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from src.Config.db import Base


class Task(Base):
    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=False)
    position = Column(Integer, nullable=False)
    points = Column(ARRAY(Integer), nullable=True)
    comments = Column(ARRAY(Integer), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="tasks")
