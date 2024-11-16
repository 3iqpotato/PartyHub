from PartyHub_Project.Party.models import Party
from PartyHub_Project.Questions.forms import QuestionForm, AnswerForm
from PartyHub_Project.Questions.models import Question
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


@login_required
def ask_question(request, party_slug):
    party = get_object_or_404(Party, slug=party_slug)

    if request.user == party.organizer:
        return redirect('details_party', slug=party_slug) #TODO NESHTO DRUGO

    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.party = party
            question.author = request.user
            question.save()

            return redirect('details_party', slug=party_slug)


@login_required
def answer_question(request, question_id, party_slug):
    question = get_object_or_404(Question, id=question_id)

    if request.user != question.party.organizer:
        return redirect('details_party', slug=party_slug)

    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()

            return redirect('details_party', slug=party_slug)
