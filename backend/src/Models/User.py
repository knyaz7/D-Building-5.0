from sqlalchemy import Column, Integer, String
from src.Config.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    fullname = Column(String(50), unique=False, nullable=False)
    password_hash = Column(String(255), nullable=False)
