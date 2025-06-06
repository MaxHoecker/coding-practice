from pydantic import BaseModel
from typing import List

class QuestionCreate(BaseModel):
    name: str
    difficulty: str
    topics: List[str]

class QuestionResponse(BaseModel):
    id: int
    name: str
    difficulty: str
    topics: List[str]