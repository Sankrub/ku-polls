from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from polls.models import Question, Choice, Vote


class VoteViewTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a test question
        self.question = Question.objects.create(question_text='Test Question', pub_date='2023-09-13')

        # Create choices for the test question
        self.choice1 = Choice.objects.create(question=self.question, choice_text='Choice 1')
        self.choice2 = Choice.objects.create(question=self.question, choice_text='Choice 2')

        # URL for the vote view
        self.url = reverse('polls:vote', args=(self.question.id,))

    def test_vote_with_authenticated_user(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate a POST request with the selected choice
        response = self.client.post(self.url, {'choice': self.choice1.id})

        # Check if the vote was recorded
        self.assertEqual(response.status_code, 302)  # Should redirect to results page
        self.assertEqual(Vote.objects.count(), 1)  # Check if a vote object was created
        self.assertEqual(Vote.objects.get().choice, self.choice1)  # Check if the correct choice was selected

    def test_vote_with_unauthenticated_user(self):
        # Simulate a POST request with the selected choice
        response = self.client.post(self.url, {'choice': self.choice2.id})

        # Check if the user is redirected to the login page (since the user is not authenticated)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login') + f'?next={self.url}')

    def test_vote_with_existing_vote(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Create an existing vote for the user and question
        existing_vote = Vote.objects.create(user=self.user, choice=self.choice1)

        # Simulate a POST request with a new choice
        response = self.client.post(self.url, {'choice': self.choice2.id})

        # Check if the vote was updated
        self.assertEqual(response.status_code, 302)  # Should redirect to results page
        self.assertEqual(Vote.objects.count(), 1)  # Only one vote object should exist
        self.assertEqual(Vote.objects.get().choice, self.choice2)  # Check if the vote was updated

    def test_vote_redirect_to_results(self):
        # Log in the user
        self.client.login(username='testuser', password='testpassword')

        # Simulate a POST request with the selected choice
        response = self.client.post(self.url, {'choice': self.choice1.id})

        # Check if the user is redirected to the results page
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('polls:results', args=(self.question.id,)))
