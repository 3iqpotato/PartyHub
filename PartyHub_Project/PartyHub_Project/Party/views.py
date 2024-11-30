import asyncio
from http.client import HTTPResponse

from PartyHub_Project.Party.forms import PartyCreateForm, PartyEditForm
from PartyHub_Project.Party.mixins import LivePartyAccessMixin
from PartyHub_Project.Party.models import Party
from PartyHub_Project.Questions.forms import AnswerForm, QuestionForm
from asgiref.sync import sync_to_async
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from rest_framework.generics import ListAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import PartySerializer

class PartyListView(ListView):
    model = Party
    paginate_by = 18  # TODO fix
    template_name = 'Party/party_list.html'

    def get_queryset(self):
        query = self.request.GET.get('q', '')
        user_filter = self.request.GET.get('filter', '')
        return Party.objects.get_parties_for_user(self.request.user, query=query, user_filter=user_filter)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # adding paginator here because we modify the queryset
        paginator = Paginator(self.get_queryset(), self.paginate_by)
        page_number = self.request.GET.get('page', 1)
        page_obj = paginator.get_page(page_number)

        context.update({
            'parties': page_obj,
            'page_obj': page_obj,
            'paginator': paginator,
            'is_paginated': page_obj.has_other_pages(),
        })

        return context


class PartyCreateView(LoginRequiredMixin, CreateView):
    model = Party
    template_name = 'Party/create_party.html'
    success_url = reverse_lazy('all_parties')
    form_class = PartyCreateForm

    def form_valid(self, form):
        # making the party organizer the user who created the party
        form.instance.organizer = self.request.user
        return super().form_valid(form)


class MyPartiesView(LoginRequiredMixin, ListView):
    model = Party
    template_name = 'Party/user_parties.html'

    def get_queryset(self):
        # getting only parties witch are created by the user
        return Party.objects.filter(organizer=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        now = timezone.localtime(timezone.now())

        # making tho types of parties not started and already ended
        context['upcoming_parties'] = self.get_queryset().filter(start_time__gte=now)
        context['past_parties'] = self.get_queryset().filter(end_time__lt=now)

        return context


class PartyDetailsView(UserPassesTestMixin, DetailView):
    model = Party
    template_name = 'Party/party_details.html'

    def get_queryset(self):
        # optimization because we show them to the user :)
        return Party.objects.select_related('organizer').prefetch_related('tickets', 'questions', 'questions__answer')

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        status = False

        if self.request.user.is_authenticated:

            context['question_form'] = QuestionForm() # adding form hor authenticated users to ask questions

            # getting the status for the user to see why he can/cant biy ticket for the party!!
            match True:
                case True if self.object.organizer == self.request.user:  # if the user is creator of the party
                    context['question_form'] = None  # removing the question form
                    context['answer_form'] = AnswerForm()  # adding form for answers
                    status = "owner"

                case True if self.object.tickets.filter(participant=self.request.user):
                    status = "have_ticket"  # the user already have a ticket

                case True if self.object.get_free_spots() == 0:
                    status = "no_spots"  # the party is full all tickets are sold

                case True if self.object.not_late_for_tickets() == False:
                    status = "late_for_tickets"  # the party deadline or start have passed

                case True if not self.object.tickets.filter(participant=self.request.user):
                    status = "can_buy"  # means everithing is okey and we can buy a ticket

        context['status'] = status

        return context

    def test_func(self): # making sure the party is not started and the user can see it
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

    def test_func(self): # making sure the user is the organizer
        user = self.request.user
        party = get_object_or_404(Party, slug=self.kwargs.get('slug'))
        return user == party.organizer and party.start_time > timezone.now()


class LivePartyDetailView(LoginRequiredMixin, LivePartyAccessMixin, DetailView):
    model = Party
    template_name = 'Party/live_party_details.html'


class PartyEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Party
    form_class = PartyEditForm
    template_name = 'Party/party_edit.html'

    def get_success_url(self):
        return reverse_lazy('details_party', kwargs={'slug': self.object.slug})

    def test_func(self):  # testing if the user is the creator of the party
        party = self.get_object()
        return self.request.user == party.organizer and party.start_time > timezone.now()


class PartyAPIListView(APIView):
    def get(self, request, *args, **kwargs):
        parties = self.get_parties()

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(parties, request, view=self)

        serializer = PartySerializer(instance=result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def get_parties(self):
        return Party.objects.get_parties_for_user(self.request.user)
