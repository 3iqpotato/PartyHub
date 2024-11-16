from django.contrib import admin

from .models import Question, Answer


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'party', 'created_at', 'get_answer')
    list_filter = ('created_at', 'party')
    search_fields = ('text', 'author__username',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)

    def get_answer(self, obj):
        return f"{obj.answer.text} | answer from  :{obj.answer.author.username}" \
            if hasattr(obj, 'answer') else 'No answer yet'
    get_answer.short_description = 'Answer'


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'author', 'question', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'author__username', 'question__text')
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
