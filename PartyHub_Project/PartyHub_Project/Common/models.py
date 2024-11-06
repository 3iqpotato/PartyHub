from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class Comment(models.Model):
    author = models.ForeignKey(
        to=get_user_model(),  # Връзка с потребителя, който е написал коментара
        on_delete=models.CASCADE,
        related_name='comments',
    )
    party = models.ForeignKey(
        to='Party.Party',  # Връзка с модела за парти
        on_delete=models.CASCADE,
        related_name='comments',
    )
    content = models.TextField(
        blank=False,
        null=False,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    def __str__(self):
        return f'Comment from {self.author} for {self.party}'

    class Meta:
        ordering = ['-created_at']  # Коментарите ще се показват по ред на създаване (най-новите първо)
