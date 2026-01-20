from sys import exception
from zoneinfo import ZoneInfo

from schemas import QuestionResponse
from services.sqlite_database import SQLiteDatabase
from models import UserAttempt, User, Status
from datetime import datetime, timezone
import random

class UserAttemptService:
    def __init__(self, db: SQLiteDatabase):
        self.db = db

    def get_utc_now_iso_format(self) -> str:
        local_tz = ZoneInfo("America/New_York")
        now_local = datetime.now(local_tz)
        naive_now_utc = now_local.astimezone(timezone.utc).replace(tzinfo=None)
        return naive_now_utc.isoformat()
    
    def get_question(self, user_id: str) -> dict | None:
        """Get a question for the user and log the attempt"""

        user = self.get_user(user_id)

        selected_question_id = self.get_user_aware_question_id(user)

        if selected_question_id is None:
            return None

        question = self.db.get_question(selected_question_id)

        # Create user attempt record
        attempt = UserAttempt(
            user_id=user.id,
            question_id=selected_question_id,
            status="started",
            timestamp=self.get_utc_now_iso_format()
        )

        self.db.create_user_attempt(attempt)

        # Convert to schema response
        question_response = QuestionResponse.from_model(question)

        return {
            "message": "Question retrieved",
            "userId": user_id,
            "question": question_response.model_dump()
        }

    def get_user_aware_question_id(self, user: User) -> int | None:
        attempted_disabled=False
        completed_disabled=False

        attempted_question_pool = self.db.get_valid_attempted_question_by_user(user.id, user.attempted_timing_days)
        completed_question_pool = self.db.get_valid_completed_question_by_user(user.id, user.completed_timing_days)

        if user.attempted_weight == 0 or len(attempted_question_pool) == 0:
            attempted_disabled=True
        if user.completed_weight == 0 or len(completed_question_pool) == 0:
            completed_disabled=True

        status_to_choose = self.calculate_user_question_status(user, attempted_disabled=attempted_disabled, completed_disabled=completed_disabled)

        if status_to_choose is None:
            return None

        if status_to_choose == Status.ATTEMPTED:
            return attempted_question_pool[random.randint(0, len(attempted_question_pool))]
        elif status_to_choose == Status.COMPLETED:
            return completed_question_pool[random.randint(0, len(completed_question_pool))]

        new_question_pool = self.db.get_new_question_ids_for_user(user.id)

        return new_question_pool[random.randint(0, len(new_question_pool))]



    # maybe move this into an object?
    def calculate_user_question_status(self, user: User, random_index=-1, attempted_disabled=False, completed_disabled=False) -> str | None:
        new_question_weight = user.new_question_weight
        attempted_weight = user.attempted_weight
        completed_weight = user.completed_weight

        if attempted_disabled:
            attempted_weight = 0

        if completed_disabled:
            completed_weight = 0

        if attempted_disabled and completed_disabled:
            return Status.NEW.value

        new_question_range = new_question_weight
        attempted_range = attempted_weight + new_question_range
        completed_range = completed_weight + attempted_range

        if random_index == -1:
            random_index = random.randrange(0, completed_range)

        if random_index < new_question_range:
            return Status.NEW.value
        if random_index < attempted_range:
            return Status.ATTEMPTED.value
        if random_index < completed_range:
            return Status.COMPLETED.value
        return None

    def get_user(self, user_id) -> User:
        user = self.db.get_user(user_id)

        if user is None:
            user = User(
                id=user_id,
                created_at=datetime.now().isoformat()
            )
            self.db.create_user(user)

        return user

    
    def change_question_status(self, user_id: str, status: str) -> dict:
        """Change the status of the user's current question attempt"""
        # Get the user's most recent attempt
        user_attempts = self.db.get_user_attempts_by_user(user_id)
        
        if not user_attempts:
            return {"error": "No attempts found for user"}
        
        # Get the most recent attempt (assuming sorted by creation order)
        latest_attempt = user_attempts[-1]

        # Create new attempt status
        new_attempt = UserAttempt(
            user_id=user_id,
            question_id=latest_attempt.question_id,
            status=status,
            timestamp=self.get_utc_now_iso_format()
        )
        
        result = self.db.create_user_attempt(new_attempt)
        
        if result:
            return {
                "message": "Status updated successfully",
                "userId": user_id,
                "status": status
            }
        else:
            return {"error": "Failed to update status"}