from django.shortcuts import render
from django.http import HttpResponse, Http404
from .models import *
from django.template import loader

# Create your views here.


def index(request):
    return HttpResponse("This is index of language_evaluator")


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

