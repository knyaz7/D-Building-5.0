from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.Config.db import Base


class User(Base):
    __tablename__ = 'command_user'

    command_id = Column(Integer, ForeignKey('command.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    role_id = Column(Integer, default=1)
    rating = Column(Integer, nullable=True)

    user = relationship("User", back_populates="commands")
    command = relationship("Command", back_populates="users")
