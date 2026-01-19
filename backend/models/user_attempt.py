from dataclasses import dataclass

@dataclass
class UserAttempt:
    user_id: str
    question_id: str
    status: str
    timestamp: str