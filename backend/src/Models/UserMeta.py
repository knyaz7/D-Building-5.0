from sqlalchemy import Column, Integer, DateTime, ARRAY, ForeignKey
from sqlalchemy.orm import relationship
from src.Config.db import Base


class UserMeta(Base):
    __tablename__ = 'users_meta'

    id = Column(Integer, primary_key=True)
    employed_at = Column(DateTime, nullable=False)
    stack = Column(ARRAY(Integer))
    position_id = Column(Integer, ForeignKey("position.id"))
