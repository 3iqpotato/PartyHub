from PartyHub_Project.Party.models import Party
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404, render
from django.utils import timezone
from django.http import HttpResponseForbidden


class LivePartyAccessMixin:

    def dispatch(self, request, *args, **kwargs):

        party = (
            Party.objects
            .select_related('organizer')
            .prefetch_related('tickets__participant')
            .get(slug=self.kwargs.get('slug'))
        ) # optimization because we use the tickets and the organizer and the tickets user

        # party = get_object_or_404(Party, slug=self.kwargs.get('slug'))

        current_time = timezone.now()

        # Проверка дали потребителят е организаторът и партито е на живо
        if request.user == party.organizer:

            if party.start_time <= current_time <= party.end_time:
                return super().dispatch(request, *args, **kwargs)
            else:
                return render(request, 'Party/party_inactive.html', {'party': party})

        # Ако партито не е на живо, показваме съобщение или шаблон
        raise PermissionDenied("You do not have permission to access this party.")
