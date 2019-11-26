from django.db import models
from django.contrib.auth.models import User
from django.utils.timesince import timesince
from django.utils import timezone
from .constants import *
from .validators import validate_audio_extension, validate_image_extension


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

    SINGLE_ANSWER = 0
    MULTIPLE_ANSWER = 1
    TRUE_FALSE_ANSWER = 2
    WRITTEN_ANSWER = 3
    SPOKEN_ANSWER = 4

    ANSWER_TYPES = (
        (SINGLE_ANSWER, 'Single'),
        (MULTIPLE_ANSWER, 'Multiple'),
        (TRUE_FALSE_ANSWER, 'True/False'),
        (WRITTEN_ANSWER, 'Written'),
        (SPOKEN_ANSWER, 'Spoken')
    )

    language = models.ForeignKey(Language, on_delete=models.CASCADE)
    question_text = models.CharField(max_length=200, blank=False)
    competence_level = models.IntegerField(blank=False, choices=COMPETENCES)
    answer_type = models.IntegerField(blank=False, choices=ANSWER_TYPES, default=SINGLE_ANSWER)
    audio_file = models.FileField(blank=True, upload_to="audio",
                                  validators=[validate_audio_extension],
                                  help_text='Supported extensions: .mp3')
    image_file = models.ImageField(blank=True, upload_to="images",
                                   validators=[validate_image_extension],
                                   help_text='Supported extensions: .png, .jpg, .jpeg, .bmp, .gif')

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


class TestPreset(models.Model):
    name = models.CharField(max_length=50, blank=False, unique=True)
    duration = models.IntegerField(default=30, blank=False)

    def __str__(self):
        return self.name


class TestPresetQuestion(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    test_preset = models.ForeignKey(TestPreset, on_delete=models.CASCADE)
