from pydantic import BaseModel
from models import Question as QuestionModel


class QuestionResponse(BaseModel):
    id: int
    titleSlug: str

    @classmethod
    def from_model(cls, question: QuestionModel) -> "QuestionResponse":
        """Factory method to convert Question dataclass to QuestionResponse schema"""
        return cls(
            id=question.id,
            titleSlug=question.titleSlug
        )