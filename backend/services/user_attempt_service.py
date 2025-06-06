from services.csv_database import CSVDatabase
from models import UserAttempt
from typing import Optional
from datetime import datetime
import uuid

class UserAttemptService:
    def __init__(self, db: CSVDatabase):
        self.db = db
    
    def get_question(self, user_id: str) -> dict:
        """Get a question for the user and log the attempt"""
        # For now, just get the first available question
        questions = self.db.get_all_questions()
        if not questions:
            return {"message": "No questions available"}
        
        question = questions[0]  # Simple logic - get first question
        
        # Create user attempt record
        attempt = UserAttempt(
            id=str(uuid.uuid4()),
            user_id=user_id,
            question_id=str(question.id),
            status="started",
            timestamp=datetime.now().isoformat()
        )
        
        self.db.create_user_attempt(attempt)
        
        return {
            "message": "Question retrieved",
            "userId": user_id,
            "question": {
                "id": question.id,
                "name": question.name,
                "difficulty": question.difficulty,
                "topics": question.topics
            }
        }
    
    def change_question_status(self, user_id: str, status: str) -> dict:
        """Change the status of the user's current question attempt"""
        # Get the user's most recent attempt
        user_attempts = self.db.get_user_attempts_by_user(user_id)
        
        if not user_attempts:
            return {"error": "No attempts found for user"}
        
        # Get the most recent attempt (assuming sorted by creation order)
        latest_attempt = user_attempts[-1]
        
        # Update the attempt status
        updated_attempt = UserAttempt(
            id=latest_attempt.id,
            user_id=latest_attempt.user_id,
            question_id=latest_attempt.question_id,
            status=status,
            timestamp=datetime.now().isoformat()
        )
        
        result = self.db.update_user_attempt(latest_attempt.id, updated_attempt)
        
        if result:
            return {
                "message": "Status updated successfully",
                "userId": user_id,
                "status": status
            }
        else:
            return {"error": "Failed to update status"}