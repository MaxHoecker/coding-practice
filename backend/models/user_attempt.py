from dataclasses import dataclass

@dataclass
class UserAttempt:
    user_id: str
    question_id: int
    status: str
    timestamp: str