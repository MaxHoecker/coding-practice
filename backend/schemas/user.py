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