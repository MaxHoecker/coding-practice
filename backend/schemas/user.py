from pydantic import BaseModel
from models import User as UserModel


class UserCreate(BaseModel):
    pass


class UserResponse(BaseModel):
    id: str
    created_at: str

    @classmethod
    def from_model(cls, user: UserModel) -> "UserResponse":
        """Factory method to convert User dataclass to UserResponse schema"""
        return cls(
            id=user.id,
            created_at=user.created_at
        )


class PercentagesRequest(BaseModel):
    new: int
    attempted: int
    completed: int


class TimingRequest(BaseModel):
    attemptedDelay: int
    completedDelay: int


class DifficultyRequest(BaseModel):
    easy: bool
    medium: bool
    hard: bool


class UserSettingsRequest(BaseModel):
    percentages: PercentagesRequest
    timing: TimingRequest
    difficulty: DifficultyRequest


class UserSettingsResponse(BaseModel):
    percentages: PercentagesRequest
    timing: TimingRequest
    difficulty: DifficultyRequest

    @classmethod
    def from_model(cls, user: UserModel) -> "UserSettingsResponse":
        """Factory method to convert User dataclass to UserSettingsResponse schema"""
        return cls(
            percentages=PercentagesRequest(
                new=user.new_question_weight,
                attempted=user.attempted_weight,
                completed=user.completed_weight
            ),
            timing=TimingRequest(
                attemptedDelay=user.attempted_timing_days,
                completedDelay=user.completed_timing_days
            ),
            difficulty=DifficultyRequest(
                easy=user.easy_difficulty,
                medium=user.medium_difficulty,
                hard=user.hard_difficulty
            )
        )