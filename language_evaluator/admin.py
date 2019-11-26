from django.contrib import admin
from .models import Question, Answer, Language, Test, TestPreset, TestPresetQuestion


class AnswerInLine(admin.TabularInline):
    model = Answer


class QuestionAdmin(admin.ModelAdmin):
    inlines = [
        AnswerInLine,
    ]
    list_display = ('question_text', 'language', 'competence_level', 'answer_type')
    list_filter = ['language', 'competence_level', 'answer_type']


class TestPresetQuestionInLine(admin.TabularInline):
    model = TestPresetQuestion


class TestPresetAdmin(admin.ModelAdmin):
    inlines = [
        TestPresetQuestionInLine,
    ]
    list_display = ('name', 'duration')


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Language)
admin.site.register(Test)
admin.site.register(TestPreset, TestPresetAdmin)
