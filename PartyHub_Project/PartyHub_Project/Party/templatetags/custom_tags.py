from django import template
from django.contrib.auth import get_user_model

register = template.Library()
UserProfile = get_user_model()


@register.simple_tag
def get_live_events(request):
    user = request.user
    live_event = UserProfile.objects.get_user_live_party(user)
    return live_event

@register.simple_tag
def get_tickets_for_party_by_check_variable(party, variable):
    tickets = party.tickets.filter(checked=variable)
    return tickets


@register.simple_tag
def build_url(request, **kwargs):

    query_params = request.GET.copy()

    for key, value in kwargs.items():
        if value:
            query_params[key] = value
        else:
            query_params.pop(key, None)
    return f"?{query_params.urlencode()}"
