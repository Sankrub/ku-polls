import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    """
    Represents a question in the polls app.

    Attributes:
        question_text (str): The text of the question.
        pub_date (datetime): The date the question was published.
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField("date published")

    def was_published_recently(self):
        """
        Checks if the question was published recently.

        Returns:
            bool: True if the question was published within the last day, False otherwise.
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

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
