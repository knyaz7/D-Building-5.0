from sqlalchemy import Column, Integer, DateTime, ARRAY, ForeignKey, String, Float
from src.Config.db import Base


class UserMeta(Base):
    __tablename__ = 'users_meta'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    position_id = Column(Integer, ForeignKey("positions.id"))
    description = Column(String, nullable=False)
    stack = Column(ARRAY(Integer), default=list)
    employed_at = Column(DateTime(timezone=True), nullable=False)
    rating = Column(Float, nullable=True)
