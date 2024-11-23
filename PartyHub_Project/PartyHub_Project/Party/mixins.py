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
        )  # optimization because we use the tickets and the organizer and the tickets user

        current_time = timezone.now()

        # checks if the party is organized by the current user
        if request.user == party.organizer:
            #  checks iif the party is live
            if party.start_time <= current_time <= party.end_time:
                return super().dispatch(request, *args, **kwargs)
            else:  # if not live
                return render(request, 'Party/party_inactive.html', {'party': party})

        # if not the organizer
        raise PermissionDenied("You do not have permission to access this party.")