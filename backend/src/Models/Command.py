from sqlalchemy import Column, Integer, String
from src.Config.db import Base


class Command(Base):
    __tablename__ = 'commands'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
