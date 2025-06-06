from dataclasses import dataclass

@dataclass
class UserAttempt:
    id: str
    user_id: str
    question_id: str
    status: str
    timestamp: str