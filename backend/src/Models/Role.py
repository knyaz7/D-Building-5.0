from sqlalchemy import Column, Integer, String
from src.Config.db import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(30), unique=True, nullable=False)
