from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required
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
        Handle the poll that is available for voting.
        If not available, show error messages and redirect to the index page.

        Args:
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.

        Returns:
            Rendered HTML page displaying the poll details or a redirect to the index page.

        """
        question = get_object_or_404(Question, pk=kwargs['pk'])

        # Check if the user has already voted for this question
        selected_choice = None
        try:
            vote = Vote.objects.get(user=request.user, choice__question=question)
            selected_choice = vote.choice
        except Vote.DoesNotExist:
            pass

        if not question.can_vote():
            messages.error(request, "This poll is not allowed for voting.")
            return redirect('polls:index')

        return render(request, 'polls/detail.html', {
            'question': question,
            'selected_choice': selected_choice,  # Pass the selected choice to the template
        })


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"

    def get_context_data(self, **kwargs):
        """
        Get the context data for rendering the view.

        This method retrieves the confirmation message from the messages framework
        and adds it to the context data, making it available for rendering in the template.

        Args:
            **kwargs: Additional keyword arguments passed to the method.

        Returns:
            dict: A dictionary containing the context data, including the confirmation message.
        """
        context = super().get_context_data(**kwargs)

        # Retrieve the confirmation message from messages framework
        confirmation_message = messages.get_messages(self.request)
        context['confirmation_message'] = confirmation_message

        return context


@login_required
def vote(request, question_id):
    """Handles the voting for a question's choices."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form with an error message.
        messages.error(request, "You didn't select a choice.")
        return render(request, 'polls/detail.html', {'question': question})

    this_user = request.user
    try:
        # Find a vote for this user and this question.
        vote = Vote.objects.get(user=this_user, choice__question=question)
        vote.choice = selected_choice
    except Vote.DoesNotExist:
        # No matching vote - create a new vote.
        vote = Vote(user=this_user, choice=selected_choice)

    vote.save()

    # Add a success message with the selected choice's name.
    messages.success(request, f'Your selected "{selected_choice.choice_text}".')

    return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))
