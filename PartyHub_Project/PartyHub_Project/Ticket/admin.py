from PartyHub_Project.Ticket.models import Ticket
from django.contrib import admin


# Register your models here.
@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('participant', 'is_vip', 'checked')
    search_fields = ('participant',)

