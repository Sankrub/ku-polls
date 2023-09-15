from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .models import Choice, Question, Vote


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")[:]
        # return Question.objects.filter(pub_date__lte=timezone.now()).exclude(
        #     end_date__lt=timezone.now()).order_by("pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())

    def get(self, request, *args, **kwargs):
        """
        Handle the poll that available for vote.
        If not available show error messages and redirect to index page.

        Args: *args: Additional positional arguments.
              **kwargs: Additional keyword arguments.

        Returns:
            Rendered HTML page displaying the poll details or a redirect to the index page.

        """
        question = get_object_or_404(Question, pk=kwargs['pk'])
        if not question.can_vote():
            messages.error(request, "This poll is not allow voting.")
            return redirect('polls:index')
        return render(request, 'polls/detail.html', {'question': question})


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


@login_required
def vote(request, question_id):
    """Handles the voting for a question's choices."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })

    this_user = request.user
    try:
        # Find a vote for this user and this question.
        vote = Vote.objects.get(user=this_user, choice__question=question)
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # No matching vote - create a new vote.
        vote = Vote(user=this_user, choice=selected_choice)
    vote.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

    # TODO: Use messages to display a confirmation on the result page.
