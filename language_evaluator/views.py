from django.http import HttpResponse, Http404, HttpResponseRedirect
from .models import *
from django.template import loader
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth import login, authenticate, get_user
from .functions.test_utils import *
from .functions.speechToText import *
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


def finish(request, test_id):
    t = get_object_or_404(Test, pk=test_id)
    if User.is_authenticated:
        if get_user(request).get_username() == t.user.username:
            if not t.is_finished:
                t.is_finished = True
                t.result = calculate_result(t)
                t.save(update_fields=['result', 'is_finished'])
            if t.is_finished:
                return HttpResponseRedirect(reverse('index', args=(),))


def test(request, test_id):
    t = get_object_or_404(Test, pk=test_id)
    if User.is_authenticated:
        if get_user(request) == t.user:
            if t.time_left().total_seconds() <= 0 and not t.is_finished:
                t.is_finished = True
                t.result = calculate_result(t)
                t.save(update_fields=['result', 'is_finished'])

            if t.is_finished:
                return HttpResponseRedirect(reverse('index', args=(),))

            q = get_object_or_404(Question, pk=t.questions_state_list()[t.current_question][:-1])
            if request.method == 'POST':
                if 'a' in request.POST:
                    # parses single answer question
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
                    # parses multiple choice question
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
                elif 'tf' in request.POST:
                    # parses true/false question
                    hit_count = 0
                    miss_count = 0
                    for q_answer in q.answer_set.all():
                        try:
                            key = 'tf' + str(q_answer.id)
                            value = request.POST.__getitem__(key)
                            if q_answer.is_correct and value == 'T':
                                hit_count += 1
                            elif not q_answer.is_correct and value == 'F':
                                hit_count += 1
                            else:
                                miss_count += 1
                        except KeyError:
                            miss_count += 1
                    states = t.questions_state_list()
                    if hit_count > miss_count:
                        states[t.current_question] = states[t.current_question][:-1] + 'T'
                    else:
                        states[t.current_question] = states[t.current_question][:-1] + 'F'
                    t.questions_state = '-'.join(states)
                    if t.current_question + 1 < len(t.questions_state_list()):
                        t.current_question = t.current_question + 1
                    t.save(update_fields=['current_question', 'questions_state'])
                elif 'w' in request.POST:
                    # parses written input
                    written_answer = request.POST.__getitem__('w')
                    written_answer = written_answer.replace('.', '')
                    written_answer = written_answer.replace(',', '')
                    written_answer_split = written_answer.split(' ')
                    hit_count = 0
                    miss_count = 0
                    for q_answer in q.answer_set.all():
                        hit_count = 0
                        miss_count = 0
                        q_answer_split = q_answer.answer_text.split(' ')
                        counter = 0
                        for word in q_answer_split:
                            word = word.replace('.', '')
                            word = word.replace(',', '')
                            if len(written_answer_split) <= counter:
                                miss_count += 1
                            elif written_answer_split[counter] == word:
                                hit_count += 1
                            elif word == '<tag>':
                                hit_count += 1
                            else:
                                miss_count += 1
                            counter += 1
                        if hit_count > miss_count:
                            break
                    states = t.questions_state_list()
                    if hit_count > miss_count:
                        states[t.current_question] = states[t.current_question][:-1] + 'T'
                    else:
                        states[t.current_question] = states[t.current_question][:-1] + 'F'
                    t.questions_state = '-'.join(states)
                    if t.current_question + 1 < len(t.questions_state_list()):
                        t.current_question = t.current_question + 1
                    t.save(update_fields=['current_question', 'questions_state'])
                elif 's' in request.FILES:
                # parses speech input
                    transcription = text_from_speech(request.FILES.__getitem__('s'), t.user.username)
                elif 'q_picked' in request.POST:
                    t.current_question = request.POST['q_picked']
                    t.save(update_fields=['current_question'])
                return HttpResponseRedirect(reverse('test', args=(t.id, )))
            else:
                return render(request, 'language_evaluator/test.html', {'test': t, 'question': q})
    return redirect('index')

