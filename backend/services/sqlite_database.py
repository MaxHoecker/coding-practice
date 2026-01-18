import sqlite3
import os
import json
from typing import List, Optional
from models import Question, User, UserAttempt


class SQLiteDatabase:
    def __init__(self, data_dir: str = "."):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "database.db")
        self._initialize_database()

    def _get_connection(self):
        """Create a database connection with foreign key support enabled"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    def _initialize_database(self):
        """Create tables if they don't exist"""
        with self._get_connection() as conn:
            cursor = conn.cursor()

            # Create questions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS questions (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    topics TEXT NOT NULL
                )
            """)

            # Create users table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id TEXT PRIMARY KEY,
                    created_at TEXT NOT NULL
                )
            """)

            # Create user_attempts table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_attempts (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    question_id TEXT NOT NULL,
                    status TEXT NOT NULL,
                    timestamp TEXT NOT NULL,
                    FOREIGN KEY (user_id) REFERENCES users(id),
                    FOREIGN KEY (question_id) REFERENCES questions(id)
                )
            """)

            # Create index for better query performance
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_user_attempts_user_id
                ON user_attempts(user_id)
            """)

            conn.commit()

    # Question CRUD operations
    def create_question(self, question: Question) -> Question:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO questions (id, name, difficulty, topics) VALUES (?, ?, ?, ?)",
                (question.id, question.name, question.difficulty, json.dumps(question.topics))
            )
            conn.commit()
        return question

    def get_question(self, question_id: int) -> Optional[Question]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, name, difficulty, topics FROM questions WHERE id = ?",
                (question_id,)
            )
            row = cursor.fetchone()

            if row:
                return Question(
                    id=row[0],
                    name=row[1],
                    difficulty=row[2],
                    topics=json.loads(row[3])
                )
        return None

    def get_all_questions(self) -> List[Question]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, name, difficulty, topics FROM questions")
            rows = cursor.fetchall()

            return [
                Question(
                    id=row[0],
                    name=row[1],
                    difficulty=row[2],
                    topics=json.loads(row[3])
                )
                for row in rows
            ]

    def update_question(self, question_id: int, updated_question: Question) -> Optional[Question]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE questions SET name = ?, difficulty = ?, topics = ? WHERE id = ?",
                (updated_question.name, updated_question.difficulty,
                 json.dumps(updated_question.topics), question_id)
            )
            conn.commit()

            if cursor.rowcount > 0:
                return updated_question
        return None

    def delete_question(self, question_id: int) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM questions WHERE id = ?", (question_id,))
            conn.commit()
            return cursor.rowcount > 0

    # User CRUD operations
    def create_user(self, user: User) -> User:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO users (id, created_at) VALUES (?, ?)",
                (user.id, user.created_at)
            )
            conn.commit()
        return user

    def get_user(self, user_id: str) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, created_at FROM users WHERE id = ?",
                (user_id,)
            )
            row = cursor.fetchone()

            if row:
                return User(id=row[0], created_at=row[1])
        return None

    def get_all_users(self) -> List[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, created_at FROM users")
            rows = cursor.fetchall()

            return [User(id=row[0], created_at=row[1]) for row in rows]

    def update_user(self, user_id: str, updated_user: User) -> Optional[User]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE users SET created_at = ? WHERE id = ?",
                (updated_user.created_at, user_id)
            )
            conn.commit()

            if cursor.rowcount > 0:
                return updated_user
        return None

    def delete_user(self, user_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            return cursor.rowcount > 0

    # UserAttempt CRUD operations
    def create_user_attempt(self, attempt: UserAttempt) -> UserAttempt:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_attempts (id, user_id, question_id, status, timestamp) VALUES (?, ?, ?, ?, ?)",
                (attempt.id, attempt.user_id, attempt.question_id, attempt.status, attempt.timestamp)
            )
            conn.commit()
        return attempt

    def get_user_attempt(self, attempt_id: str) -> Optional[UserAttempt]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, user_id, question_id, status, timestamp FROM user_attempts WHERE id = ?",
                (attempt_id,)
            )
            row = cursor.fetchone()

            if row:
                return UserAttempt(
                    id=row[0],
                    user_id=row[1],
                    question_id=row[2],
                    status=row[3],
                    timestamp=row[4]
                )
        return None

    def get_user_attempts_by_user(self, user_id: str) -> List[UserAttempt]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, user_id, question_id, status, timestamp FROM user_attempts WHERE user_id = ? ORDER BY timestamp",
                (user_id,)
            )
            rows = cursor.fetchall()

            return [
                UserAttempt(
                    id=row[0],
                    user_id=row[1],
                    question_id=row[2],
                    status=row[3],
                    timestamp=row[4]
                )
                for row in rows
            ]

    def get_all_user_attempts(self) -> List[UserAttempt]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, user_id, question_id, status, timestamp FROM user_attempts")
            rows = cursor.fetchall()

            return [
                UserAttempt(
                    id=row[0],
                    user_id=row[1],
                    question_id=row[2],
                    status=row[3],
                    timestamp=row[4]
                )
                for row in rows
            ]

    def update_user_attempt(self, attempt_id: str, updated_attempt: UserAttempt) -> Optional[UserAttempt]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE user_attempts SET user_id = ?, question_id = ?, status = ?, timestamp = ? WHERE id = ?",
                (updated_attempt.user_id, updated_attempt.question_id,
                 updated_attempt.status, updated_attempt.timestamp, attempt_id)
            )
            conn.commit()

            if cursor.rowcount > 0:
                return updated_attempt
        return None

    def delete_user_attempt(self, attempt_id: str) -> bool:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM user_attempts WHERE id = ?", (attempt_id,))
            conn.commit()
            return cursor.rowcount > 0
