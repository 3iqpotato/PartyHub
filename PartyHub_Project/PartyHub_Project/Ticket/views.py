
from PartyHub_Project.Party.models import Party
from PartyHub_Project.Ticket.models import Ticket
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.http import JsonResponse, HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView, DetailView, DeleteView

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
    @staticmethod
    def check_conditions(request, party):
        if not party.is_public:
            if not request.user.is_following(party.organizer) or not party.organizer.is_following(request.user):
                raise PermissionDenied("you are not allowed to come to this party.")

        if party.registration_deadline and party.registration_deadline < timezone.now():
            raise PermissionDenied("too late to buy.")

        if party.start_time and party.start_time < timezone.now():
            raise PermissionDenied("The party already started.")

        if party.get_free_spots() <= 0:
            raise PermissionDenied("no free spaces.")

        if Ticket.objects.filter(participant=request.user, party=party).exists():
            raise PermissionDenied("already have a ticket.")

    def get(self, request, party_slug):
        party = get_object_or_404(Party, slug=party_slug)

        self.check_conditions(request, party)

        return render(request, 'Ticket/ticket_create.html', {'party': party})

    def post(self, request, party_slug):
        party = get_object_or_404(Party, slug=party_slug)

        self.check_conditions(request, party)

        ticket = Ticket.objects.create(participant=request.user, party=party, is_vip=request.user.is_vip())
        ticket.save()

        return redirect('details_party', slug=party_slug)


class TicketDetailsView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Ticket
    template_name = 'Ticket/ticket_details.html'
    context_object_name = 'ticket'

    def test_func(self):
        ticket = self.get_object()
        return ticket.participant == self.request.user


class TicketDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Ticket
    template_name = 'Ticket/ticket_delete.html'

    def get_success_url(self):
        return reverse_lazy('user_tickets', kwargs={'pk': self.request.user.pk})

    def test_func(self):
        ticket = self.get_object()
        return ticket.participant == self.request.user


def mark_as_arrived(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user == ticket.party.organizer and request.method == 'POST':

        ticket.mark_as_arrived()

        return JsonResponse({
            'ticket': {
                'id': ticket.id,
                'new_action_url': reverse('mark_as_not_arrived', args=[ticket.id]),
                'new_button_text': "Mark as Not Arrived"
            }
        })
    return HttpResponseForbidden("You are not authorized to perform this action.")


def mark_as_not_arrived(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if request.user == ticket.party.organizer and request.method == 'POST':
        ticket.mark_as_not_arrived()

        return JsonResponse({
            'ticket': {
                'id': ticket.id,
                'new_action_url': reverse('mark_as_arrived', args=[ticket.id]),
                'new_button_text': "Mark as Arrived"
            }
        })
    return HttpResponseForbidden("You are not authorized to perform this action.")
