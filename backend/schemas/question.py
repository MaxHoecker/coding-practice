from pydantic import BaseModel
from models import Question as QuestionModel


class QuestionCreate(BaseModel):
    questionFrontendId: int
    paidOnly: bool
    title: str
    titleSlug: str
    difficulty: str
    acRate: float


class QuestionResponse(BaseModel):
    id: int
    questionFrontendId: int
    paidOnly: bool
    title: str
    titleSlug: str
    difficulty: str
    acRate: float

    @classmethod
    def from_model(cls, question: QuestionModel) -> "QuestionResponse":
        """Factory method to convert Question dataclass to QuestionResponse schema"""
        return cls(
            id=question.id,
            questionFrontendId=question.questionFrontendId,
            paidOnly=question.paidOnly,
            title=question.title,
            titleSlug=question.titleSlug,
            difficulty=question.difficulty,
            acRate=question.acRate
        )