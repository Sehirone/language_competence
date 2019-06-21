from django.contrib import admin
from .models import Question, Answer, Language, Test


class AnswerInLine(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInLine,
    ]
    list_display = ('question_text', 'language', 'competence_level')
    list_filter = ['language', 'competence_level']


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Language)
admin.site.register(Test)
