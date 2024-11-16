from PartyHub_Project.Party.forms import PartyCreateForm, PartyEditForm
from PartyHub_Project.Party.models import Party
from django.contrib import admin

# Register your models here.


@admin.register(Party)
class PartyAdmin(admin.ModelAdmin):
    list_display = ('title', 'organizer', 'start_time', 'party_type', 'tickets_count')
    search_fields = ('title',)
    list_filter = ('party_type', 'start_time',)
    ordering = ('-start_time',)
    add_form = PartyCreateForm
    form = PartyEditForm

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = self.add_form
        else:
            kwargs['form'] = self.form
        return super().get_form(request, obj, **kwargs)

    @staticmethod
    def tickets_count(obj):
        return obj.tickets.count()
