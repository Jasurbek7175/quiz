from django.contrib import admin
from .models import Question, Quiz, Category, Answer, SubCategory


class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 1  #
    fields = ['content', 'correct']
    verbose_name = "Ответ"
    verbose_name_plural = "Ответы"


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ['content', 'category']
    list_filter = ['category']
    search_fields = ['content']
    inlines = [AnswerInline]


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ['content', 'question', 'correct']
    list_filter = ['correct']
    search_fields = ['content', 'question__content']

# Register other models


admin.site.register(Quiz)
admin.site.register(Category)
admin.site.register(SubCategory)
