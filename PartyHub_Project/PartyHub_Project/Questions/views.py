from PartyHub_Project.Party.models import Party
from PartyHub_Project.Questions.forms import QuestionForm, AnswerForm
from PartyHub_Project.Questions.models import Question
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect


@login_required
def ask_question(request, party_slug):
    # Вземаме събитието, за което ще се задава въпрос
    party = get_object_or_404(Party, slug=party_slug)

    # Проверка дали потребителят не е организатор на партито
    if request.user == party.organizer:
        return redirect('details_party', slug=party_slug) #TODO NESHTO DRUGO

    # Обработваме формата за въпрос
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
    # Вземаме въпроса, на който ще отговаряме
    question = get_object_or_404(Question, id=question_id)

    # Проверяваме дали потребителят е организатор на партито
    if request.user != question.party.organizer:
        return redirect('details_party', slug=party_slug)

    # Обработваме формата за отговор
    if request.method == 'POST':
        form = AnswerForm(request.POST)
        if form.is_valid():
            # Създаваме отговор, като го свързваме с въпроса
            answer = form.save(commit=False)
            answer.question = question
            answer.author = request.user
            answer.save()

            return redirect('details_party', slug=party_slug)
