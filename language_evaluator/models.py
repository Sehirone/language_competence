from django.db import models
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.utils import timezone
from .constants import *


class Language(models.Model):
    name = models.CharField(max_length=30, blank=False, unique=True)
    short_name = models.CharField(max_length=5, blank=False)

    def __str__(self):
        return self.name + '(' + self.short_name + ')'


class Question(models.Model):
    COMPETENCE_A1 = 0
    COMPETENCE_A2 = 1
    COMPETENCE_B1 = 2
    COMPETENCE_B2 = 3
    COMPETENCE_C1 = 4
    COMPETENCE_C2 = 5

    COMPETENCES = (
        (COMPETENCE_A1, 'A1'),
        (COMPETENCE_A2, 'A2'),
        (COMPETENCE_B1, 'B1'),
        (COMPETENCE_B2, 'B2'),
        (COMPETENCE_C1, 'C1'),
        (COMPETENCE_C2, 'C2')
    )

    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, blank=False)
    competence_level = models.IntegerField(blank=False, choices=COMPETENCES)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer_text = models.CharField(max_length=80, blank=False)
    is_correct = models.BooleanField(blank=False)

    def __str__(self):
        return self.answer_text


class Test(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField('start time')
    questions_state = models.CharField(max_length=400, blank=False)
    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    current_question = models.IntegerField(default=0)
    is_finished = models.BooleanField(default=False)
    result = models.FloatField(default=0)

    def __str__(self):
        return self.language.__str__()

    def questions_state_list(self):
        return self.questions_state.split('-')

    def time_left(self):
        return (self.start_time + timezone.timedelta(minutes=TIME_FOR_TEST_MINUTES)) - timezone.now()

    def time_left_readable(self):
        return timesince(timezone.now(), self.start_time + timezone.timedelta(minutes=TIME_FOR_TEST_MINUTES))

    def time_since_last(self):
        return timesince(self.start_time, timezone.now())
