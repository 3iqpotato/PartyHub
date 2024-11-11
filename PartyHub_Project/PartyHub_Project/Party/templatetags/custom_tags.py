from django import template


register = template.Library()

@register.simple_tag
def get_live_events(request):
    user = request.user

    live_event = user.get_live_party()
    return live_event

@register.simple_tag
def get_tickets_for_party_by_check_variable(party, variable):
    tickets = party.tickets.filter(checked=variable)
    return tickets
