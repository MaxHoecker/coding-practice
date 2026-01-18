import csv
import os
from typing import List, Optional
from models import Question, User, UserAttempt

class CSVDatabase:
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.questions_file = os.path.join(data_dir, "questions.csv")
        self.users_file = os.path.join(data_dir, "users.csv")
        self.user_attempts_file = os.path.join(data_dir, "userAttempts.csv")
        self._ensure_files_exist()
    
    def _ensure_files_exist(self):
        if not os.path.exists(self.questions_file):
            with open(self.questions_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'difficulty', 'topics'])
        
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'created_at'])
        
        if not os.path.exists(self.user_attempts_file):
            with open(self.user_attempts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'user_id', 'question_id', 'status', 'timestamp'])
    
    def create_question(self, question: Question) -> Question:
        with open(self.questions_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                question.id,
                question.name,
                question.difficulty,
                '|'.join(question.topics)
            ])
        return question
    
    def get_question(self, question_id: int) -> Optional[Question]:
        with open(self.questions_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if int(row['id']) == question_id:
                    return Question(
                        id=int(row['id']),
                        name=row['titleSlug'],
                        difficulty=row['difficulty'],
                        topics=row['topicTags'].split('|')
                    )
        return None
    
    def get_all_questions(self) -> List[Question]:
        questions = []
        with open(self.questions_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                questions.append(Question(
                    id=int(row['id']),
                    name=row['titleSlug'],
                    difficulty=row['difficulty'],
                    topics=row['topicTags'].split('|')
                ))
        return questions
    
    def update_question(self, question_id: int, updated_question: Question) -> Optional[Question]:
        questions = self.get_all_questions()
        updated = False
        
        for i, q in enumerate(questions):
            if q.id == question_id:
                questions[i] = updated_question
                updated = True
                break
        
        if updated:
            with open(self.questions_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'difficulty', 'topics'])
                for q in questions:
                    writer.writerow([
                        q.id,
                        q.name,
                        q.difficulty,
                        '|'.join(q.topics)
                    ])
            return updated_question
        return None
    
    def delete_question(self, question_id: int) -> bool:
        questions = self.get_all_questions()
        original_count = len(questions)
        questions = [q for q in questions if q.id != question_id]
        
        if len(questions) < original_count:
            with open(self.questions_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'name', 'difficulty', 'topics'])
                for q in questions:
                    writer.writerow([
                        q.id,
                        q.name,
                        q.difficulty,
                        '|'.join(q.topics)
                    ])
            return True
        return False
    
    def create_user(self, user: User) -> User:
        with open(self.users_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([user.id, user.created_at])
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        with open(self.users_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == user_id:
                    return User(
                        id=row['id'],
                        created_at=row['created_at']
                    )
        return None
    
    def get_all_users(self) -> List[User]:
        users = []
        with open(self.users_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users.append(User(
                    id=row['id'],
                    created_at=row['created_at']
                ))
        return users
    
    def update_user(self, user_id: str, updated_user: User) -> Optional[User]:
        users = self.get_all_users()
        updated = False
        
        for i, u in enumerate(users):
            if u.id == user_id:
                users[i] = updated_user
                updated = True
                break
        
        if updated:
            with open(self.users_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'created_at'])
                for u in users:
                    writer.writerow([u.id, u.created_at])
            return updated_user
        return None
    
    def delete_user(self, user_id: str) -> bool:
        users = self.get_all_users()
        original_count = len(users)
        users = [u for u in users if u.id != user_id]
        
        if len(users) < original_count:
            with open(self.users_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'created_at'])
                for u in users:
                    writer.writerow([u.id, u.created_at])
            return True
        return False
    
    def create_user_attempt(self, attempt: UserAttempt) -> UserAttempt:
        with open(self.user_attempts_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                attempt.id,
                attempt.user_id,
                attempt.question_id,
                attempt.status,
                attempt.timestamp
            ])
        return attempt
    
    def get_user_attempt(self, attempt_id: str) -> Optional[UserAttempt]:
        with open(self.user_attempts_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == attempt_id:
                    return UserAttempt(
                        id=row['id'],
                        user_id=row['user_id'],
                        question_id=row['question_id'],
                        status=row['status'],
                        timestamp=row['timestamp']
                    )
        return None
    
    def get_user_attempts_by_user(self, user_id: str) -> List[UserAttempt]:
        attempts = []
        with open(self.user_attempts_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['user_id'] == user_id:
                    attempts.append(UserAttempt(
                        id=row['id'],
                        user_id=row['user_id'],
                        question_id=row['question_id'],
                        status=row['status'],
                        timestamp=row['timestamp']
                    ))
        return attempts
    
    def get_all_user_attempts(self) -> List[UserAttempt]:
        attempts = []
        with open(self.user_attempts_file, 'r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                attempts.append(UserAttempt(
                    id=row['id'],
                    user_id=row['user_id'],
                    question_id=row['question_id'],
                    status=row['status'],
                    timestamp=row['timestamp']
                ))
        return attempts
    
    def update_user_attempt(self, attempt_id: str, updated_attempt: UserAttempt) -> Optional[UserAttempt]:
        attempts = self.get_all_user_attempts()
        updated = False
        
        for i, a in enumerate(attempts):
            if a.id == attempt_id:
                attempts[i] = updated_attempt
                updated = True
                break
        
        if updated:
            with open(self.user_attempts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'user_id', 'question_id', 'status', 'timestamp'])
                for a in attempts:
                    writer.writerow([
                        a.id,
                        a.user_id,
                        a.question_id,
                        a.status,
                        a.timestamp
                    ])
            return updated_attempt
        return None
    
    def delete_user_attempt(self, attempt_id: str) -> bool:
        attempts = self.get_all_user_attempts()
        original_count = len(attempts)
        attempts = [a for a in attempts if a.id != attempt_id]
        
        if len(attempts) < original_count:
            with open(self.user_attempts_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['id', 'user_id', 'question_id', 'status', 'timestamp'])
                for a in attempts:
                    writer.writerow([
                        a.id,
                        a.user_id,
                        a.question_id,
                        a.status,
                        a.timestamp
                    ])
            return True
        return False