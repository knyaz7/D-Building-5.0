from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from src.Config.db import Base


class Point(Base):
    __tablename__ = 'points'

    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    status = Column(Boolean, default=False)
