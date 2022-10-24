from django.contrib import admin
from django.utils.html import mark_safe
from .models import Choice, Question, Test


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3
    exclude = ('votes',)


class QuestionInline(admin.StackedInline):
    model = Question
    extra = 2


@admin.register(Test)
class TestAdmin(admin.ModelAdmin):
    list_display = ('testtype', 'level', 'pub_date', 'maxballs')
    fieldsets = [
        (None,               {'fields': ['testtype']}),
        ('Дата публикации', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ('Максимальное кол-во баллов', {'fields': ['maxballs']})
    ]
    inlines = [QuestionInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'link', 'testnumb', 'queue')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('К какому тесту относится', {'fields': ['testnumb']}),
        ('Очередь в тесте ', {'fields': ['queue']})
    ]
    inlines = [ChoiceInline]

    @admin.display(description='Ссылка на вопрос')
    def link(self, question: Question):
        return mark_safe(f'''<a href="/polls/{question.pk}" target="_blank">Открыть</a>''')
