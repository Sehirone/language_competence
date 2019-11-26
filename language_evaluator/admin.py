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
    save_as = True


class TestAdmin(admin.ModelAdmin):
    readonly_fields = ('result', 'questions_state', 'current_question', 'is_finished')

    def save_model(self, request, obj, form, change):
        obj.questions_state = ""
        for q in obj.test_preset.testpresetquestion_set.all():
            obj.questions_state += str(q.id) + "N-"
        obj.questions_state = obj.questions_state[:-1]
        obj.current_question = 0
        obj.result = 0
        obj.is_finished = False
        super().save_model(request, obj, form, change)


# Register your models here.
admin.site.register(Question, QuestionAdmin)
admin.site.register(Language)
admin.site.register(Test, TestAdmin)
admin.site.register(TestPreset, TestPresetAdmin)
