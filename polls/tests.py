import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Question


def create_question(question_text, days):
    """
    Create a question with the given `question_text` and published the
    given number of `days` offset to now (negative for questions published
    in the past, positive for questions that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """
        If no questions exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("polls:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_past_question(self):
        """
        Questions with a pub_date in the past are displayed on the
        index page.
        """
        question = create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )

    def test_future_question(self):
        """
        Questions with a pub_date in the future aren't displayed on
        the index page.
        """
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertContains(response, "No polls are available.")
        self.assertQuerySetEqual(response.context["latest_question_list"], [])

    def test_future_question_and_past_question(self):
        """
        Even if both past and future questions exist, only past questions
        are displayed.
        """
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse("polls:index"))
        self.assertQuerySetEqual(
            response.context["latest_question_list"],
            [question],
        )


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """
        The detail view of a question with a pub_date in the future
        returns a 404 not found.
        """
        future_question = create_question(question_text="Future question.", days=5)
        url = reverse("polls:detail", args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """
        The detail view of a question with a pub_date in the past
        displays the question's text.
        """
        past_question = create_question(question_text="Past Question.", days=-5)
        url = reverse("polls:detail", args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)


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
