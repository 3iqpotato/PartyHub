from django.apps import AppConfig


class EventConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PartyHub_Project.Party'

    def ready(self):
        import PartyHub_Project.Party.signals