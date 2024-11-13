from django.shortcuts import render

# Create your views here.
# views.py
from django.urls import reverse_lazy
from django.views.generic.edit import FormView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from .models import Party, Question
from .forms import QuestionForm


class AskQuestionView(LoginRequiredMixin, FormView):
    form_class = QuestionForm
    template_name = 'ask_question.html'

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'slug': self.kwargs['slug']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        party = get_object_or_404(Party, id=self.kwargs['party_id'])
        context['party'] = party
        return context

    def form_valid(self, form):
        party = get_object_or_404(Party, id=self.kwargs['party_id'])

        # Проверяваме дали потребителят не е организатор на партито
        if self.request.user == party.organizer:
            return self.form_invalid(form)

        # Записваме въпроса
        question = form.save(commit=False)
        question.party = party
        question.user = self.request.user
        question.save()

        return super().form_valid(form)


class AnswerQuestionView(LoginRequiredMixin, FormView):
    form_class = AnswerForm
    template_name = 'answer_question.html'

    def get_success_url(self):
        return reverse_lazy('details', kwargs={'party_id': self.kwargs['party_id']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        question = get_object_or_404(Question, id=self.kwargs['question_id'])
        context['question'] = question
        return context

    def form_valid(self, form):
        question = get_object_or_404(Question, id=self.kwargs['question_id'])

        # Проверяваме дали потребителят е организатор на партито
        if self.request.user != question.party.organizer:
            return self.form_invalid(form)

        # Записваме отговора
        answer = form.save(commit=False)
        answer.question = question
        answer.user = self.request.user
        answer.save()

        return super().form_valid(form)