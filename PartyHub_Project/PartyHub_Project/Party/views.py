from PartyHub_Project.Party.forms import PartyCreateForm, PartyEditForm
from PartyHub_Project.Party.mixins import LivePartyAccessMixin
from PartyHub_Project.Party.models import Party
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.paginator import Paginator
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import ListView, CreateView, DetailView, DeleteView, UpdateView
from rest_framework.pagination import PageNumberPagination
from rest_framework.views import APIView
from .serializers import PartySerializer
from .views_helpers import check_party_started_and_request_user_is_organizer, test_user_can_see_party_details, \
    update_context_and_get_status_for_party_details


class PartyListView(ListView):
    model = Party
    paginate_by = 18
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        form.instance.organizer = self.request.user
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        self.object = None
        return super().form_invalid(form)


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
        party = self.object
        return update_context_and_get_status_for_party_details(self.request, party, context)


    def test_func(self): # making sure the party is not started and the user can see it
        party = self.get_object()
        return test_user_can_see_party_details(party, self.request)


class PartyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Party
    template_name = 'Party/party_delete.html'
    success_url = reverse_lazy('user_parties')

    def test_func(self): # making sure the user is the organizer
        party = self.get_object()
        return self.request.user == party.organizer


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
        return check_party_started_and_request_user_is_organizer(party, self.request.user)


class PartyAPIListView(APIView):
    def get(self, request, *args, **kwargs):
        parties = self.get_parties()

        paginator = PageNumberPagination()
        result_page = paginator.paginate_queryset(parties, request, view=self)

        serializer = PartySerializer(instance=result_page, many=True)

        return paginator.get_paginated_response(serializer.data)

    def get_parties(self):
        return Party.objects.get_parties_for_user(self.request.user)
