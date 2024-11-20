from PartyHub_Project.Questions.models import Answer, Question
from django import forms
from django.forms import models


class AnswerForm(models.ModelForm):
    class Meta:
        model = Answer
        fields = ('text',)

        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Enter Answer',
            }),}



class QuestionForm(models.ModelForm):
    class Meta:
        model = Question
        fields = ('text',)

        widgets = {
            'text': forms.TextInput(attrs={
                'placeholder': 'Ask Question',
            }),}
