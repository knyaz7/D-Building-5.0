from sqlalchemy import Column, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

from src.Config.db import Base


class CommandUser(Base):
    __tablename__ = 'command_user'

    command_id = Column(Integer, ForeignKey('commands.id'), primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    role_id = Column(Integer, default=1)
    rating = Column(Float, nullable=True)
