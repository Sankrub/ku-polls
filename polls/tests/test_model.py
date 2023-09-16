import datetime
from django.test import TestCase
from django.utils import timezone
from polls.models import Question


class QuestionModelTests(TestCase):

    def test_is_published_with_future_pub_date(self):
        """
        is_published() should return False for a question with a future pub_date.
        """
        future_date = timezone.now() + timezone.timedelta(days=30)
        future_question = Question(pub_date=future_date)
        self.assertIs(future_question.is_published(), False)

    def test_was_published_recently_with_future_question(self):
        """
        was_published_recently() returns False for questions whose pub_date
        is in the future.
        """
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_is_published_default_pub_date(self):
        """
        is_published() should return True for a question with the default pub_date (now).
        """
        current_time = timezone.now()
        current_question = Question(pub_date=current_time)
        self.assertTrue(current_question.is_published())

    def test_is_published_past_pub_date(self):
        """
        is_published() should return True for a question with a pub_date in the past.
        """
        past_date = timezone.now() - timezone.timedelta(days=1)
        past_question = Question(pub_date=past_date)
        self.assertTrue(past_question.is_published())

    def test_can_vote_future_end_date(self):
        """
        can_vote() should return True for a question with a future end_date.
        """
        future_date = timezone.now() + timezone.timedelta(days=1)
        future_question = Question(end_date=future_date)
        self.assertTrue(future_question.can_vote())

    def test_can_vote_default_end_date(self):
        """
        can_vote() should return True for a question with the default end_date (None).
        """
        current_time = timezone.now()
        current_question = Question(end_date=None)
        self.assertTrue(current_question.can_vote())

    def test_can_vote_past_end_date(self):
        """
        can_vote() should return False for a question with a past end_date.
        """
        past_date = timezone.now() - timezone.timedelta(days=1)
        past_question = Question(end_date=past_date)
        self.assertFalse(past_question.can_vote())
