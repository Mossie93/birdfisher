from django.shortcuts import get_object_or_404, render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Choice, Question

# Create your views here.
def index(request):
    latest_questions_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_questions_list': latest_questions_list}
    return render(request, 'polls/index.html', context)
    # Behind  the scenes
    # template = loader.get_template('polls/index.html')
    # context = { 'latest_questions_list': latest_questions_list }
    # return HttpResponse(template.render(context, request))

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    # behind the scenes
    # raise Http404("Question does not exist")
    # Http404 is from django.http module
    return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls.results.html', {'question': question})

def vote(request, question_id):
    question =  get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.chocie_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice"
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
    return HttpResponseRedirect(reverse('polls:results', args=(question.id)))
