from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.Config.db import Base


class Tool(Base):
    __tablename__ = 'tools'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
