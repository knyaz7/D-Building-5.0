from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from src.Config.db import Base


class Comment(Base):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    text = Column(String(255), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="comments")
