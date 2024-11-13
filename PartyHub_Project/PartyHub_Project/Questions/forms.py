from PartyHub_Project.Questions.models import Answer, Question
from django.forms import models


class AnswerForm(models.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)


class QuestionForm(models.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)
