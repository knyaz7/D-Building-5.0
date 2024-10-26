from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from src.Config.db import Base


class Position(Base):
    __tablename__ = 'positions'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)

    comments = relationship("UserMeta", back_populates="position")
