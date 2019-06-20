from django.db import models


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

    question_text = models.CharField(max_length=200, blank=False, unique=True)
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

