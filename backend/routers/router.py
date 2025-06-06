from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.csv_database import CSVDatabase
from services.user_attempt_service import UserAttemptService

router = APIRouter()

# Initialize services
db = CSVDatabase()
user_attempt_service = UserAttemptService(db)

class StatusRequest(BaseModel):
    status: str

@router.get("/question")
async def get_question(x_user_id: Optional[str] = Header(None, alias="X-User-ID")):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")
    
    result = user_attempt_service.get_question(x_user_id)
    return result

@router.post("/completed")
async def post_completed(
    request: StatusRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")
    
    result = user_attempt_service.change_question_status(x_user_id, request.status)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result