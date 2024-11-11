from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Ticket(models.Model):
    party = models.ForeignKey(to='Party.Party', on_delete=models.CASCADE, related_name='tickets')
    participant = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='tickets')
    is_vip = models.BooleanField(default=False)
    checked = models.BooleanField(default=False)

    def mark_as_arrived(self):
        if not self.checked:
            self.checked = True
            self.participant.points += 5
            self.participant.save()
            self.save()

    def mark_as_not_arrived(self):
        if self.checked:
            self.checked = False
            self.participant.points -= 5
            if self.participant.points < 0:
                self.participant.points = 0  # За да не стават точките отрицателни
            self.participant.save()
            self.save()

    def __str__(self):
        ticket_type = "VIP" if self.is_vip else "Standard"
        return f"{ticket_type} Ticket for {self.party.title} - {self.participant.username}"


