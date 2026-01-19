from dataclasses import dataclass
from typing import List

@dataclass
class Question:
    id: int
    questionFrontendId: int
    paidOnly: bool
    title: str
    titleSlug: str
    difficulty: str
    acRate: float

