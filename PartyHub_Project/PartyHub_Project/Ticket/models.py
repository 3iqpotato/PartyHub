from django.db import models

# Create your models here.

class Ticket(models.Model):
    event = models.ForeignKey(to='Party.Party', on_delete=models.CASCADE, related_name='tickets')
    participant = models.ForeignKey(to='Accounts.UserProfile', on_delete=models.CASCADE, related_name='tickets')
    is_vip = models.BooleanField(default=False)

    def __str__(self):
        ticket_type = "VIP" if self.is_vip else "Standard"
        return f"{ticket_type} Ticket for {self.event.title} - {self.participant.username}"


