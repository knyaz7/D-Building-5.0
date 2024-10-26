from sqlalchemy import Column, Integer, String, ARRAY
from src.Config.db import Base


class Stage(Base):
    __tablename__ = 'stages'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    tasks = Column(ARRAY(Integer), default=list)
