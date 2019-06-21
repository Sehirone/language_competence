from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm
# Create your views here.


def index(request):
    template = loader.get_template('language_evaluator/index.html')
    context = {

    }
    return HttpResponse(template.render(context, request))


def question(request, question_id):
    try:
        question = Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")

    answer_set = question.answer_set.all()
    template = loader.get_template('language_evaluator/question.html')
    context = {
        'question': question,
        'answer_set': answer_set,
    }

    return HttpResponse(template.render(context, request))


def answer(request, question_id):
    question = get_object_or_404(Question, pk=question_id)

    try:
        selected_choice = question.answer_set.get(pk=request.POST['a'])
    except (KeyError, Answer.DoesNotExist):
        # Redisplay the question voting form.
        answer_set = question.answer_set.all()
        return render(request, 'language_evaluator/question.html', {
            'question': question,
            'answer_set': answer_set,
            'error_message': "You didn't select a choice.",
        })
    else:
        return HttpResponseRedirect(reverse('answer_result', args=(question_id, selected_choice.id)))


def answer_result(request, question_id, answer_id):
    question = get_object_or_404(Question, pk=question_id)
    answer = get_object_or_404(Answer, pk=answer_id)
    return render(request, 'language_evaluator/answer_result.html', {'question': question, 'answer': answer})


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = RegisterForm()
    return render(request, 'language_evaluator/register.html', {'form': form})
