from pydantic import BaseModel

class UserAttemptCreate(BaseModel):
    question_id: str
    status: str

class UserAttemptResponse(BaseModel):
    id: str
    user_id: str
    question_id: str
    status: str
    timestamp: str