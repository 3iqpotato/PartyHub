from PartyHub_Project.Questions.models import Answer, Question
from django import forms
from django.forms import models


class AnswerForm(models.ModelForm):
    text = forms.CharField(
        label='Answer',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter Answer...',
            'class': 'answer_form',
        }),
        )

    class Meta:
        model = Answer
        fields = ('text',)


class QuestionForm(models.ModelForm):
    text = forms.CharField(
        label='Your Question',
        widget=forms.Textarea(attrs={
            'placeholder': 'Enter Question...',
        }),
    )

    class Meta:
        model = Question
        fields = ('text',)

