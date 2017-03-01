from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Choice, Question


class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'
    queryset = Question.objects.order_by('-pub_date')[:5]
    '''def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by('-pub_date')[:5]'''


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):

        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
    
def add_question(request):
    return render(request, 'polls/add_question.html')

def create_question(request):
    try:
        question = request.POST['question']
        if not question.strip():
            raise
    except :
        return render(request, 'polls/add_question.html', 
                {'error_message': "You didn't add question",})
    else:
        q = Question(question_text = question, pub_date = timezone.now())
        q.save()
        return HttpResponseRedirect(reverse('polls:add_choice', args=(q.id,)))
    
def add_choice(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/add_choice.html', {
            'question': question },)

def create_choice(request, question_id):
    if 'cancel' in request.POST:
        return HttpResponseRedirect(reverse('polls:index',))
    else:
        q = get_object_or_404(Question, pk=question_id)
        try:
            choice = request.POST['choice']
            if not choice.strip():
                raise
        except :
            return render(request, 'polls/add_choice.html', 
                {'question': q, 'message': "You didn't add choice",})
        else:
            q.choice_set.create(choice_text=choice, votes=0)
            if 'add' in request.POST:
                return render(request, 'polls/add_choice.html', 
                {'question': q, 'message': "Your choice has been added",})
            elif 'finish' in request.POST:
                return HttpResponseRedirect(reverse('polls:index',))