from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from typing import Optional
from services.sqlite_database import SQLiteDatabase
from services.user_attempt_service import UserAttemptService
from schemas import UserSettingsRequest, UserSettingsResponse

router = APIRouter()

# Initialize services
db = SQLiteDatabase()
user_attempt_service = UserAttemptService(db)

class StatusRequest(BaseModel):
    status: str

@router.get("/question")
async def get_question(x_user_id: Optional[str] = Header(None, alias="X-User-ID")):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")
    
    result = user_attempt_service.get_question(x_user_id)

    if result is None:
        raise HTTPException(status_code=404, detail=f"No questions could be found")

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

@router.get("/user/settings")
async def get_settings(x_user_id: Optional[str] = Header(None, alias="X-User-ID")):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")

    # Get or auto-create user (existing pattern)
    user = user_attempt_service.get_user(x_user_id)

    # Convert to response schema
    settings_response = UserSettingsResponse.from_model(user)

    return settings_response

@router.post("/user/settings")
async def post_settings(
    request: UserSettingsRequest,
    x_user_id: Optional[str] = Header(None, alias="X-User-ID")
):
    if not x_user_id:
        raise HTTPException(status_code=400, detail="X-User-ID header is required")

    try:
        # Update settings with validation
        updated_user = user_attempt_service.update_user_settings(x_user_id, request)

        # Return updated settings as confirmation
        settings_response = UserSettingsResponse.from_model(updated_user)
        return settings_response

    except ValueError as e:
        # Validation error (percentages, difficulty)
        raise HTTPException(status_code=400, detail=str(e))

    except Exception as e:
        # Database or other error
        raise HTTPException(status_code=500, detail="Failed to save settings")