import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Represents a question in the polls app.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date the question was published.
        end_date (datetime): The date the question is closed (optional).
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published", default=timezone.now)
    end_date = models.DateTimeField("date closed", default=None, null=True, blank=True)

    def was_published_recently(self):
        """
        Checks if the question was published recently.

        Returns:
            bool: True if the question was published within the last day, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """
        Checks if the question is already published by checking with current time.

        Returns:
            bool: True if time the published time is less than current time.
        """
        return timezone.now() >= self.pub_date

    def can_vote(self):
        """
        Check if the current time is between published time and close time.
        :return:
        """
        if self.end_date is not None:
            return self.pub_date <= timezone.now() <= self.end_date
        else:
            return self.pub_date <= timezone.now()

    def __str__(self):
        """
        Returns a string representation of the question.

        Returns:
            str: The text of the question.
        """
        return self.question_text


class Choice(models.Model):
    """
    Represents a choice for a poll question.

    Attributes:
        question (Question): The question to which this choice belongs.
        choice_text (str): The text of the choice.
        votes (int): The number of votes received for this choice.
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """
        Returns a string representation of the choice.

        Returns:
            str: The text of the choice.
        """
        return self.choice_text
