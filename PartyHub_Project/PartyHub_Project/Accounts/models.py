from PartyHub_Project.Accounts.managers import UserProfileManager
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
# Doing that to
class BaseUser(AbstractUser):

    objects = UserProfileManager()
    """
    Extends Django's AbstractUser to create a base user model.
    The one-to-one relationship with UserProfile allows us to optimize database queries
    by using `select_related` or `prefetch_related` to fetch user and profile data in a single query,
    reducing the number of database queries and improving performance.
    """


class UserProfile(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='profile')
    points = models.PositiveIntegerField(default=0)
    is_vip = models.BooleanField(default=False)
    friends = models.ManyToManyField('self', blank=True, symmetrical=True)

    def __str__(self):
        return self.user.username


class Friendship(models.Model):
    user = models.ForeignKey(to=BaseUser, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(to=BaseUser, on_delete=models.CASCADE, related_name='friends')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend}"