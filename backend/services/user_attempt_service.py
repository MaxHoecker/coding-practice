from schemas import QuestionResponse
from services.sqlite_database import SQLiteDatabase
from models import UserAttempt, User
from datetime import datetime
import random

class UserAttemptService:
    def __init__(self, db: SQLiteDatabase):
        self.db = db
    
    def get_question(self, user_id: str) -> dict | None:
        """Get a question for the user and log the attempt"""

        user = self.db.get_user(user_id)

        if user is None:
            user = User(
                id=user_id,
                created_at=datetime.now().isoformat()
            )
            self.db.create_user(user)

        questions = self.db.get_all_questions()
        if not questions:
            return None

        question = questions[random.randrange(0, len(questions))]  # Simple logic - get random question

        # Create user attempt record
        attempt = UserAttempt(
            user_id=user_id,
            question_id=str(question.id),
            status="started",
            timestamp=datetime.now().isoformat()
        )

        self.db.create_user_attempt(attempt)

        # Convert to schema response
        question_response = QuestionResponse.from_model(question)

        return {
            "message": "Question retrieved",
            "userId": user_id,
            "question": question_response.model_dump()
        }
    
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
            timestamp=datetime.now().isoformat()
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