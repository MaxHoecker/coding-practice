from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    id: int
    name: str
    difficulty: str
    topics: List[str]