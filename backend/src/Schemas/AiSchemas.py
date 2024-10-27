from pydantic import BaseModel
from typing import List

class AiInput(BaseModel):
    master_task_id: int
    stack: List[int]
