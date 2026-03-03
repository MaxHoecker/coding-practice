import sqlite3
import os
from typing import List, Optional
from models import Question, User, UserAttempt, Status


class SQLiteDatabase:
    def __init__(self, data_dir: str = "./database"):
        self.data_dir = data_dir
        self.db_path = os.path.join(data_dir, "database.db")

    def _get_connection(self):
        """Create a database connection with foreign key support enabled"""
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA foreign_keys = ON")
        return conn

    # Question CRUD operations
    def get_question(self, question_id: int) -> Optional[Question]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, questionFrontendId, paidOnly, title, titleSlug, difficulty, acRate FROM questions WHERE id = ?",
                (question_id,)
            )
            row = cursor.fetchone()

            if row:
                return Question(
                    id=row[0],
                    questionFrontendId=row[1],
                    paidOnly=bool(row[2]),
                    title=row[3],
                    titleSlug=row[4],
                    difficulty=row[5],
                    acRate=row[6]
                )
        return None

    def get_all_questions(self) -> List[Question]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, questionFrontendId, paidOnly, title, titleSlug, difficulty, acRate FROM questions WHERE paidOnly = FALSE")
            rows = cursor.fetchall()

            return [
                Question(
                    id=row[0],
                    questionFrontendId=row[1],
                    paidOnly=bool(row[2]),
                    title=row[3],
                    titleSlug=row[4],
                    difficulty=row[5],
                    acRate=row[6]
                )
                for row in rows
            ]

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
            cursor.execute("""
                SELECT id, created_at, new_question_weight, attempted_weight,
                       completed_weight, easy_difficulty, medium_difficulty,
                       hard_difficulty, attempted_timing_days, completed_timing_days,
                       view_paid_only
                FROM users WHERE id = ?
            """, (user_id,))
            row = cursor.fetchone()

            if row:
                return User(
                    id=row[0],
                    created_at=row[1],
                    new_question_weight=row[2],
                    attempted_weight=row[3],
                    completed_weight=row[4],
                    easy_difficulty=bool(row[5]),
                    medium_difficulty=bool(row[6]),
                    hard_difficulty=bool(row[7]),
                    attempted_timing_days=row[8],
                    completed_timing_days=row[9],
                    view_paid_only=bool(row[10])
                )
        return None

    def update_user(self, user: User) -> User:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users SET
                    new_question_weight = ?,
                    attempted_weight = ?,
                    completed_weight = ?,
                    easy_difficulty = ?,
                    medium_difficulty = ?,
                    hard_difficulty = ?,
                    attempted_timing_days = ?,
                    completed_timing_days = ?,
                    view_paid_only = ?
                WHERE id = ?
            """, (
                user.new_question_weight,
                user.attempted_weight,
                user.completed_weight,
                user.easy_difficulty,
                user.medium_difficulty,
                user.hard_difficulty,
                user.attempted_timing_days,
                user.completed_timing_days,
                user.view_paid_only,
                user.id
            ))
            conn.commit()
        return user

    # UserAttempt CRUD operations
    def create_user_attempt(self, attempt: UserAttempt) -> UserAttempt:
        print(attempt)
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO user_attempts (user_id, question_id, status, timestamp) VALUES (?, ?, ?, ?)",
                (attempt.user_id, attempt.question_id, attempt.status, attempt.timestamp)
            )
            conn.commit()
        return attempt

    def get_user_attempts_by_user(self, user_id: str) -> List[UserAttempt]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, question_id, status, timestamp FROM user_attempts WHERE user_id = ? ORDER BY timestamp",
                (user_id,)
            )
            rows = cursor.fetchall()

            return [
                UserAttempt(
                    user_id=row[0],
                    question_id=row[1],
                    status=row[2],
                    timestamp=row[3]
                )
                for row in rows
            ]

    # Make aware of other user fields
    def get_new_question_ids_for_user(self, user_id: str) -> List[int]:
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT q.id
                FROM questions q
                JOIN users u ON u.id = ?
                LEFT JOIN user_attempts ua ON q.id = ua.question_id AND ua.user_id = ?
                WHERE (ua.status = 'started' OR ua.status IS NULL)
                  AND q.paidOnly = 0
                  AND (
                    (u.easy_difficulty = 1 AND q.difficulty = 'EASY') OR
                    (u.medium_difficulty = 1 AND q.difficulty = 'MEDIUM') OR
                    (u.hard_difficulty = 1 AND q.difficulty = 'HARD')
                  )
            """, (user_id, user_id))
            rows = cursor.fetchall()

            return [row[0] for row in rows]

    # Make unique on question id
    def get_valid_attempted_question_by_user(self, user_id: str, attempted_before_days: int) -> List[int]:
        datetime_str = '-'+str(attempted_before_days)+" days"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ua.question_id
                FROM user_attempts ua
                JOIN questions q ON ua.question_id = q.id
                JOIN users u ON u.id = ua.user_id
                WHERE ua.user_id = ?
                  AND ua.timestamp < strftime('%Y-%m-%dT%H:%M:%S.%f', 'now', ?)
                  AND ua.status = ?
                  AND q.paidOnly = 0
                  AND (
                    (u.easy_difficulty = 1 AND q.difficulty = 'EASY') OR
                    (u.medium_difficulty = 1 AND q.difficulty = 'MEDIUM') OR
                    (u.hard_difficulty = 1 AND q.difficulty = 'HARD')
                  )
            """, (user_id, datetime_str, Status.ATTEMPTED.value))
            rows = cursor.fetchall()

            return [row[0] for row in rows]

    # Make unique on question id
    def get_valid_completed_question_by_user(self, user_id: str, completed_before_days: int) -> List[int]:
        datetime_str = '-' + str(completed_before_days) + " days"
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ua.question_id
                FROM user_attempts ua
                JOIN questions q ON ua.question_id = q.id
                JOIN users u ON u.id = ua.user_id
                WHERE ua.user_id = ?
                  AND ua.timestamp < strftime('%Y-%m-%dT%H:%M:%S.%f', 'now', ?)
                  AND ua.status = ?
                  AND q.paidOnly = 0
                  AND (
                    (u.easy_difficulty = 1 AND q.difficulty = 'EASY') OR
                    (u.medium_difficulty = 1 AND q.difficulty = 'MEDIUM') OR
                    (u.hard_difficulty = 1 AND q.difficulty = 'HARD')
                  )
            """, (user_id, datetime_str, Status.COMPLETED.value))
            rows = cursor.fetchall()

            return [row[0] for row in rows]