from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'PartyHub_Project.Accounts'

    def ready(self):
        import PartyHub_Project.Accounts.signals  # Импортирай сигналите