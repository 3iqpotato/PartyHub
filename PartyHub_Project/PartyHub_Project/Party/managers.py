from django.db import models
from django.utils import timezone


class PartyManager(models.Manager):
    # def filter_by_organizer(self, organizer):
    #     return self.filter(organizer__) TODO to make it search by organizator name

    def get_current_parties(self, user):
        now = timezone.now()
        return self.filter(organizer=user, date__lte=now, end_date__gte=now)

    def get_public_parties(self):
        return self.filter(is_public=True)