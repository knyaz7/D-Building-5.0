from sqlalchemy import Column, Integer, String, DateTime, Float
from Config.db import Base
import datetime


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    created_at = Column(DateTime(), default=datetime.datetime.utcnow())
    rating = Column(Float, nullable=True)
