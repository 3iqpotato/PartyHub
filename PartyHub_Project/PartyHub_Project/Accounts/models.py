from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models

User = get_user_model()

# Create your models here.
class UserProfile(AbstractUser):
    points = models.PositiveIntegerField(default=0)
    is_vip = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)


    def __str__(self):
        return self.username





class Friendship(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(to=User, on_delete=models.CASCADE, related_name='friends')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend}"