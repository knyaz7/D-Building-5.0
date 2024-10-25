from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class UserOutput(BaseModel):
    id: int
    username: str
    password_hash: str
    created_at: datetime
    rating: Optional[float] = None
