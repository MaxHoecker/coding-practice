import unittest

from models import User
from question_status import Status
from user_attempt_service import UserAttemptService


class TestUserAttemptService(unittest.TestCase):

    def test_default_user_question_distribution(self):
        user = User(
            id="my_user_id",
            created_at="1/19/2026",
            new_question_weight=50,
            attempted_weight=30,
            completed_weight=20
        )

        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 0), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 49), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 50), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 79), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 80), Status.COMPLETED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 99), Status.COMPLETED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 100), None)

    def test_user_question_distribution_with_single_0_weight(self):
        user = User(
            id="my_user_id",
            created_at="1/19/2026",
            new_question_weight=50,
            attempted_weight=0,
            completed_weight=50
        )

        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 0), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 49), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 50), Status.COMPLETED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 99), Status.COMPLETED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 100), None)

    def test_user_question_distribution_with_double_0_weight(self):
        user = User(
            id="my_user_id",
            created_at="1/19/2026",
            new_question_weight=0,
            attempted_weight=100,
            completed_weight=0
        )

        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 0), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 49), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 50), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 79), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 80), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 99), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 100), None)

    def test_default_user_question_distribution_attempted_disabled(self):
        user = User(
            id="my_user_id",
            created_at="1/19/2026",
            new_question_weight=50,
            attempted_weight=30,
            completed_weight=20
        )

        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 0, attempted_disabled=True), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 49, attempted_disabled=True), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 50, attempted_disabled=True), Status.COMPLETED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 69, attempted_disabled=True), Status.COMPLETED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 70, attempted_disabled=True), None)

    def test_default_user_question_distribution_completed_disabled(self):
        user = User(
            id="my_user_id",
            created_at="1/19/2026",
            new_question_weight=50,
            attempted_weight=30,
            completed_weight=20
        )

        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 0, completed_disabled=True), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 49, completed_disabled=True), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 50, completed_disabled=True), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 79, completed_disabled=True), Status.ATTEMPTED.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 80, completed_disabled=True), None)

    def test_default_user_question_distribution_both_disabled(self):
        user = User(
            id="my_user_id",
            created_at="1/19/2026",
            new_question_weight=50,
            attempted_weight=30,
            completed_weight=20
        )

        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 0, attempted_disabled=True, completed_disabled=True), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 49, attempted_disabled=True, completed_disabled=True), Status.NEW.value)
        self.assertEqual(UserAttemptService.calculate_user_question_status(user, 50, attempted_disabled=True, completed_disabled=True), Status.NEW.value)


if __name__ == '__main__':
    unittest.main()
