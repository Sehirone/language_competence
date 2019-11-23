from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, get_user
from .functions.test_utils import *
from .forms import RegisterForm
# Create your views here.


def index(request):
    template = loader.get_template('language_evaluator/index.html')
    languages = []
    if get_user(request).is_authenticated:
        for l in Language.objects.all():
            found = False
            for t in get_user(request).test_set.all():
                if l.name == t.language.name:
                    found = True
            if not found:
                languages.append(l)

    context = {
        'languages': languages,
    }
    return HttpResponse(template.render(context, request))


# TODO: Remove
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


# TODO: Remove
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


# TODO: Remove
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


def test(request, test_id):
    t = get_object_or_404(Test, pk=test_id)

    if User.is_authenticated:
        if get_user(request).get_username() == t.user.username:
            if t.time_left().total_seconds() <= 0 and not t.is_finished:
                t.is_finished = True
                t.result = calculate_result(t)
                t.save(update_fields=['result', 'is_finished'])

            if t.is_finished:
                return HttpResponseRedirect(reverse('index', args=(),))

            q = get_object_or_404(Question, pk=t.questions_state_list()[t.current_question][:-1])
            if request.method == 'POST':
                if 'a' in request.POST:
                    answer = get_object_or_404(Answer, pk=request.POST['a'])
                    states = t.questions_state_list()
                    if answer.is_correct:
                        states[t.current_question] = states[t.current_question][:-1] + 'T'
                    else:
                        states[t.current_question] = states[t.current_question][:-1] + 'F'
                    t.questions_state = '-'.join(states)
                    if t.current_question + 1 < len(t.questions_state_list()):
                        t.current_question = t.current_question + 1
                    t.save(update_fields=['current_question', 'questions_state'])
                elif 'm' in request.POST:
                    hit_count = 0
                    miss_count = 0
                    for q_answer in q.answer_set.all():
                        if str(q_answer.id) in request.POST.getlist('m'):
                            if q_answer.is_correct:
                                hit_count += 1
                            else:
                                miss_count += 1
                        else:
                            if q_answer.is_correct:
                                miss_count += 1
                            else:
                                hit_count += 1
                    states = t.questions_state_list()
                    if hit_count > miss_count:
                        states[t.current_question] = states[t.current_question][:-1] + 'T'
                    else:
                        states[t.current_question] = states[t.current_question][:-1] + 'F'
                    t.questions_state = '-'.join(states)
                    if t.current_question + 1 < len(t.questions_state_list()):
                        t.current_question = t.current_question + 1
                    t.save(update_fields=['current_question', 'questions_state'])
                elif 'q_picked' in request.POST:
                    t.current_question = request.POST['q_picked']
                    t.save(update_fields=['current_question'])
                return HttpResponseRedirect(reverse('test', args=(t.id, )))
            else:
                return render(request, 'language_evaluator/test.html', {'test': t, 'question': q})

    return redirect('index')

