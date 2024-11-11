from PartyHub_Project.Party.models import Party
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponseForbidden


class LivePartyAccessMixin:

    def dispatch(self, request, *args, **kwargs):
        # Намираме партито по `pk`
        party = get_object_or_404(Party, slug=self.kwargs.get('slug'))
        current_time = timezone.now()

        # Проверка дали потребителят е организаторът и партито е на живо
        if request.user == party.organizer:

            if party.date <= current_time <= party.end_date:
                return super().dispatch(request, *args, **kwargs)
            else:
                return render(request, 'Party/party_inactive.html', {'party': party})

        # Ако партито не е на живо, показваме съобщение или шаблон
        return HttpResponseForbidden("You do not have permission to access this party.")