from dataclasses import dataclass

@dataclass
class User:
    id: str
    created_at: str
    new_question_weight: int = 50
    attempted_weight: int = 30
    completed_weight: int = 20
    easy_difficulty: bool = True
    medium_difficulty: bool = True
    hard_difficulty: bool = False
    attempted_timing_days: int = 3
    completed_timing_days: int = 7
    view_paid_only: bool = False