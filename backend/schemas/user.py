from pydantic import BaseModel

class UserCreate(BaseModel):
    pass

class UserResponse(BaseModel):
    id: str
    created_at: str