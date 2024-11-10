from PartyHub_Project.Party.forms import PartyCreateForm
from PartyHub_Project.Party.models import Party
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, DeleteView


#not a View a function that get the right parties for the users!!!!
def return_parties_for_user(request):
    public_parties = Party.objects.get_public_parties()

    all_parties = public_parties

    if request.user.is_authenticated:
        all_parties = all_parties.exclude(
            id__in=request.user.organized_parties.values_list('id', flat=True))

        users_following = request.user.get_following()

        friends_parties = Party.objects.none()

        for follower in users_following:
            if follower.following.is_following(request.user):
                friends_parties = friends_parties | follower.following.get_not_started_parties()

        # print(friends_parties)

        if friends_parties:
            all_parties = all_parties | friends_parties

    query = request.GET.get('q', '')

    if query:
        all_parties = all_parties.filter(title__icontains=query)

    return all_parties


class PartyListView(ListView):
    model = Party
    paginate_by = 1
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

        # Филтриране на предстоящи и изтекли партита
        context['upcoming_parties'] = self.get_queryset().filter(date__gte=now)
        context['past_parties'] = self.get_queryset().filter(end_date__lt=now)

        return context


class PartyDetailsView(UserPassesTestMixin, DetailView):
    model = Party
    template_name = 'Party/party_details.html'

    def test_func(self):
        # Получаваме обекта за партито
        party = self.get_object()
        now = timezone.localtime(timezone.now())
        # Проверка дали партито е започнало
        if party.date <= now:
            return False

        # Проверка дали партито е публично
        if not party.is_public:
            # Ако партито не е публично, проверяваме връзката между текущия потребител и организатора
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
        party = Party.objects.get_party_by_id(self.kwargs.get('pk'))
        return user == party.organizer


class LivePartyDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Party
    template_name = 'Party/live_party_details.html'

    def test_func(self):
        party = Party.objects.get_party_by_id(self.kwargs.get('pk'))
        current_time = timezone.now()

        # Проверка дали потребителят е организаторът и дали партито е активно в момента
        if self.request.user == party.organizer and party.date <= current_time <= party.end_date:
            return True
        return False