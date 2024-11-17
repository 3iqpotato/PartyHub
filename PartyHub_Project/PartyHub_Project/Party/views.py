from PartyHub_Project.Party.forms import PartyCreateForm, PartyEditForm
from PartyHub_Project.Party.mixins import LivePartyAccessMixin
from PartyHub_Project.Party.models import Party
from PartyHub_Project.Questions.forms import AnswerForm, QuestionForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView


# not a View a function that get the right parties for the users!!!!
def return_parties_for_user(request):
    public_parties = Party.objects.get_public_parties().select_related('organizer')

    all_parties = public_parties

    if request.user.is_authenticated:
        all_parties = all_parties.exclude(
            id__in=request.user.organized_parties.values_list('id', flat=True))

        users_following = request.user.get_following()

        friends_parties = Party.objects.none()

        for follower in users_following:
            if follower.following.is_following(request.user):
                friends_parties = friends_parties | follower.following.get_not_started_parties()

        if friends_parties:
            all_parties = all_parties | friends_parties

    query = request.GET.get('q', '')

    if query:
        all_parties = all_parties.filter(title__icontains=query)

    return all_parties


class PartyListView(ListView):
    model = Party
    paginate_by = 1  # TODO fix
    template_name = 'Party/party_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        all_parties = return_parties_for_user(self.request)

        paginator = Paginator(all_parties, self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        # Актуализиране на контекста с страничните резултати
        context.update({
            'parties': page_obj,  # парти страницата с резултати
            'page_obj': page_obj,  # самият обект на страницата за навигация
            'paginator': paginator,  # обекта на пагинатора за общия брой страници
            'is_paginated': page_obj.has_other_pages(),  # проверка за повече страници
        })

        return context


class PartyCreateView(LoginRequiredMixin, CreateView):
    model = Party
    template_name = 'Party/create_party.html'
    success_url = reverse_lazy('all_parties')
    form_class = PartyCreateForm

    def form_valid(self, form):
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class MyPartiesView(LoginRequiredMixin, ListView):
    model = Party
    template_name = 'Party/user_parties.html'

    def get_queryset(self):
        return Party.objects.filter(organizer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.localtime(timezone.now())

        context['upcoming_parties'] = self.get_queryset().filter(start_time__gte=now)
        context['past_parties'] = self.get_queryset().filter(end_time__lt=now)

        return context


class PartyDetailsView(UserPassesTestMixin, DetailView):
    model = Party
    template_name = 'Party/party_details.html'

    def get_queryset(self):
        return Party.objects.select_related('organizer').prefetch_related('tickets', 'questions', 'questions__answer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        status = False
        if self.request.user.is_authenticated:
            context['question_form'] = QuestionForm()
            match True:
                case True if self.object.get_free_spots() == 0:
                    status = "no_spots"
                case True if self.object.not_late_for_tickets() == False:
                    status = "late_for_tickets"  # Вече е късно за билети
                case True if self.object.organizer == self.request.user:
                    context['question_form'] = None
                    context['answer_form'] = AnswerForm()
                    status = "owner"  # Потребителят е собственик на партито
                case True if not self.object.tickets.filter(participant=self.request.user):
                    status = "can_buy"
                case True if self.object.tickets.filter(participant=self.request.user):
                    status = "have_ticket"

        context['status'] = status

        return context

    def test_func(self):
        party = self.get_object()
        now = timezone.localtime(timezone.now())

        if party.end_time <= now:
            return False

        if not party.is_public:
            user = self.request.user

            if not user.is_authenticated:
                return False

            organizer = party.organizer

            if organizer == user:
                return True

            if not (user.is_following(organizer) and organizer.is_following(user)):
                return False

        return True


class PartyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Party
    template_name = 'Party/party_delete.html'
    success_url = reverse_lazy('user_parties')

    def test_func(self):
        user = self.request.user
        party = get_object_or_404(Party, slug=self.kwargs.get('slug'))
        return user == party.organizer


class LivePartyDetailView(LoginRequiredMixin, LivePartyAccessMixin, DetailView):
    model = Party
    template_name = 'Party/live_party_details.html'

    def get_queryset(self):
        return Party.objects.select_related('organizer').prefetch_related('tickets__participant')


class PartyEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Party
    form_class = PartyEditForm
    template_name = 'Party/party_edit.html'

    def get_success_url(self):
        return reverse_lazy('details_party', kwargs={'slug': self.object.slug})

    def test_func(self):
        party = self.get_object()
        return self.request.user == party.organizer and party.start_time > timezone.now()
