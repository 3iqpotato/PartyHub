from django.db import models


class EventManager(models.Manager):
    # def filter_by_organizer(self, organizer):
    #     return self.filter(organizer__) TODO to make it search by organizator name

    def filter_by_type(self, event_type):
        return self.filter(event_type=event_type)

    def filter_by_date(self, date):
        return self.filter(date__date=date)