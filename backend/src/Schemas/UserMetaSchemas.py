from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class UserMetaInput(BaseModel):
    user_id: int
    position_id: int = None
    description: str
    employed_at: datetime
    stack: Optional[List[int]] = None
    rating: Optional[float] = None


class UserMetaOutput(BaseModel):
    id: int
    user_id: int
    position_id: Optional[int] = None
    description: str
    stack: List[int]
    employed_at: datetime
    rating: Optional[float] = None

    class Config:
        orm_mode = True
        from_attributes = True
