from pydantic import BaseModel
from typing import List

class AiInput(BaseModel):
    stack: List[int] = None
