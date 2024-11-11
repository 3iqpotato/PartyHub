
from PartyHub_Project.Party.models import Party
from PartyHub_Project.Ticket.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, CreateView, DetailView, DeleteView

UserModel = get_user_model()
# Create your views here.
class UserTicketsListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Ticket
    template_name = 'Ticket/user_tickets_list.html'
    def test_func(self):
        profile = get_object_or_404(UserModel, pk=self.kwargs['pk'])
        return self.request.user == profile

    def get_context_data(self, *, object_list=None, **kwargs):
        user_tickets = self.request.user.get_valid_tickets()
        context = {'user_tickets': user_tickets}
        return context


class TicketCreateView(LoginRequiredMixin, View):
    def get(self, request, party_slug):
        # Намираме партито по slug
        party = get_object_or_404(Party, slug=party_slug)

        # Проверка дали партито е private и дали потребителят следва организатора
        if not party.is_public:
            if not request.user.is_following(party.organizer) or not party.organizer.is_following(request.user):
                return redirect('error')

        if party.registration_deadline and party.registration_deadline < timezone.now():
            return redirect('error')  # Може да добавиш съобщение за изтекъл срок

        if party.date and party.date < timezone.now():
            return redirect('error')  # Може да добавиш съобщение за започнало парти

        if party.get_free_spots() <= 0:
            return redirect('error')
        # Проверка дали потребителят вече има билет за това парти
        if Ticket.objects.filter(participant=request.user, party=party).exists():
            return redirect('error')  # Може да добавиш съобщение за вече закупен билет

        # Показваме бутон за закупуване на билет
        return render(request, 'Ticket/ticket_create.html', {'party': party})

    def post(self, request, party_slug):
        # Намираме партито по slug
        party = get_object_or_404(Party, slug=party_slug)

        # Проверка дали партито е private и дали потребителят следва организатора
        if not party.is_public:
            if not request.user.is_following(party.organizer) or not party.organizer.is_following(request.user):
                return redirect('error')

        if party.registration_deadline and party.registration_deadline < timezone.now():
            return redirect('error')  # Може да добавиш съобщение за изтекъл срок

            # Проверка дали партито вече е започнало
        if party.date and party.date < timezone.now():
            return redirect('error')

        if party.get_free_spots() <= 0:
            return redirect('error')

        # Проверка дали потребителят вече има билет за това парти
        if Ticket.objects.filter(participant=request.user, party=party).exists():
            return redirect('error')

        ticket = Ticket.objects.create(participant=request.user, party=party, is_vip=request.user.is_vip())
        ticket.save()
        # Пренасочваме към списъка с билети на потребителя
        return redirect('details_party', slug=party_slug)

class TicketDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Ticket
    template_name = 'Ticket/ticket_details.html'
    context_object_name = 'ticket'  # За да е удобно да използваме в темплейта

    def test_func(self):
        ticket = self.get_object()  # Вземаме билета чрез id от URL
        return ticket.participant == self.request.user  # Ако билета е за текущия потребител


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    template_name = 'Ticket/ticket_delete.html'
    def get_success_url(self):
        return reverse('user_tickets', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        ticket = self.get_object()  # Вземаме билета чрез id от URL
        return ticket.participant == self.request.user
