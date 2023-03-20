
from pydantic import BaseModel
from datetime import datetime
from typing import List

class PullRequest(BaseModel):
    number: int
    title: str
    user_id: str
    created_at: datetime
    labels: List[str]
    files: List[str]