from django.contrib import admin
from django.utils.html import mark_safe
import datetime
from django.utils import timezone
from .models import Choice, Question


class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'pub_date', 'link')
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Дата публикации', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    inlines = [ChoiceInline]

    @admin.display(description='Ссылка на вопрос')
    def link(self, question: Question):
        return mark_safe(f'''<a href="/polls/{question.pk}" target="_blank">Открыть</a>''')


