from PartyHub_Project.Party.models import Party
from django.shortcuts import render
from django.views.generic import ListView


# Create your views here.
class PartyListView(ListView):
    model = Party
    template_name = 'Party/party_list.html'