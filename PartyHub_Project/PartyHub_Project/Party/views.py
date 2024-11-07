from PartyHub_Project.Party.forms import PartyCreateForm
from PartyHub_Project.Party.models import Party
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView


# Create your views here.
class PartyListView(ListView):
    model = Party
    template_name = 'Party/party_list.html'

class PartyCreateView(CreateView):
    model = Party
    template_name = 'Party/create_party.html'
    success_url = reverse_lazy('all_parties')
    form_class = PartyCreateForm
