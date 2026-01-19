from pydantic import BaseModel
from models import UserAttempt as UserAttemptModel


class UserAttemptCreate(BaseModel):
    question_id: str
    status: str


class UserAttemptResponse(BaseModel):
    id: str
    user_id: str
    question_id: str
    status: str
    timestamp: str

    @classmethod
    def from_model(cls, attempt: UserAttemptModel) -> "UserAttemptResponse":
        """Factory method to convert UserAttempt dataclass to UserAttemptResponse schema"""
        return cls(
            id=attempt.id,
            user_id=attempt.user_id,
            question_id=attempt.question_id,
            status=attempt.status,
            timestamp=attempt.timestamp
        )