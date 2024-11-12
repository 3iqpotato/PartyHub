from django.db import models
from django.utils import timezone


class PartyManager(models.Manager):

    # def filter_by_organizer(self, organizer):
    #     return self.filter(organizer__) TODO to make it search by organizator name

    def get_current_parties(self, user):
        now = timezone.now()
        return self.filter(organizer=user, start_time__lte=now, end_time__gte=now)

    def get_public_parties(self):
        now = timezone.now()
        return self.filter(is_public=True, start_time__gte=now)

    def get_party_by_id(self, party_id):
        return self.filter(id=party_id).first()