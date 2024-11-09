from django import template


register = template.Library()

@register.simple_tag
def get_live_events(request):
    user = request.user
    live_event = user.get_live_party()

    # Връща първото парти, ако има такова
    return live_event # Може да върне None, ако няма парти на живо за този потребител