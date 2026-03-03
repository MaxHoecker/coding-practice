import unittest
from unittest.mock import MagicMock

from models import User, Question
from question_status import Status
from user_attempt_service import UserAttemptService

class TestUtils:
    def make_weighted_user(self, new_question_weight=50, attempted_weight=30, completed_weight=20) -> User:
        return User(id="test_user", created_at="2026-01-01", new_question_weight=new_question_weight,
                    attempted_weight=attempted_weight, completed_weight=completed_weight)

    def make_difficulty_user(self, easy=True, medium=True, hard=False) -> User:
        return User(id="test_user", created_at="2026-01-01", easy_difficulty=easy, medium_difficulty=medium, hard_difficulty=hard)

    def make_question(self, qid: int, difficulty: str) -> Question:
        return Question(id=qid, questionFrontendId=qid, paidOnly=False, title=f"Q{qid}", titleSlug=f"q{qid}", difficulty=difficulty, acRate=50.0)
    
    def make_question_list(self):
        return [self.make_question(1, "EASY"), self.make_question(2, "MEDIUM"), self.make_question(3, "HARD")]

    def make_service(self) -> UserAttemptService:
        mock_db = MagicMock()
        return UserAttemptService(mock_db)

class TestUserAttemptService(unittest.TestCase):
    service = TestUtils().make_service()

    def test_default_user_question_distribution(self):
        user = TestUtils().make_weighted_user()

        self.assertEqual(self.service.calculate_user_question_status(user, 0), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 49), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 50), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 79), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 80), Status.COMPLETED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 99), Status.COMPLETED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 100), None)

    def test_user_question_distribution_with_single_0_weight(self):
        user = TestUtils().make_weighted_user(50, 0, 50)

        self.assertEqual(self.service.calculate_user_question_status(user, 0), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 49), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 50), Status.COMPLETED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 99), Status.COMPLETED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 100), None)

    def test_user_question_distribution_with_double_0_weight(self):
        user = TestUtils().make_weighted_user(0, 100, 0)

        self.assertEqual(self.service.calculate_user_question_status(user, 0), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 49), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 50), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 79), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 80), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 99), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 100), None)

    def test_default_user_question_distribution_attempted_disabled(self):
        user = TestUtils().make_weighted_user()

        self.assertEqual(self.service.calculate_user_question_status(user, 0, attempted_disabled=True), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 49, attempted_disabled=True), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 50, attempted_disabled=True), Status.COMPLETED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 69, attempted_disabled=True), Status.COMPLETED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 70, attempted_disabled=True), None)

    def test_default_user_question_distribution_completed_disabled(self):
        user = TestUtils().make_weighted_user()

        self.assertEqual(self.service.calculate_user_question_status(user, 0, completed_disabled=True), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 49, completed_disabled=True), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 50, completed_disabled=True), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 79, completed_disabled=True), Status.ATTEMPTED.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 80, completed_disabled=True), None)

    def test_default_user_question_distribution_both_disabled(self):
        user = TestUtils().make_weighted_user()

        self.assertEqual(self.service.calculate_user_question_status(user, 0, attempted_disabled=True, completed_disabled=True), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 49, attempted_disabled=True, completed_disabled=True), Status.NEW.value)
        self.assertEqual(self.service.calculate_user_question_status(user, 50, attempted_disabled=True, completed_disabled=True), Status.NEW.value)


if __name__ == '__main__':
    unittest.main()
