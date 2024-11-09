from PartyHub_Project.Party.forms import PartyCreateForm
from PartyHub_Project.Party.models import Party
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView


# Create your views here.
class PartyListView(ListView):
    model = Party
    template_name = 'Party/party_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        followers_parties = Party.objects.none()

        user_followers = self.request.user.get_followers()
        for follower in user_followers:
            followers_parties | follower.user.organized_parties.all()

        public_parties = Party.objects.get_public_parties().exclude(id__in=self.request.user.organized_parties.values_list('id', flat=True))

        all_parties = public_parties
        if followers_parties:
            all_parties | public_parties

        query = self.request.GET.get('q', '')

        if query:
            all_parties = all_parties.filter(title__icontains=query)


        context.update({'parties': all_parties})
        return context

class PartyCreateView(LoginRequiredMixin, CreateView):
    model = Party
    template_name = 'Party/create_party.html'
    success_url = reverse_lazy('all_parties')
    form_class = PartyCreateForm

    def form_valid(self, form):
        form.instance.organizer = self.request.user

        return super().form_valid(form)
