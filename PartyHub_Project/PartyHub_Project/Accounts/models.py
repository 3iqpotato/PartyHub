from PartyHub_Project.Accounts.managers import UserProfileManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserProfile(AbstractUser):
    points = models.PositiveIntegerField(default=0)

    is_vip = models.BooleanField(default=False)

    friends = models.ManyToManyField(
        to='self',
        blank=True,
        symmetrical=True,
        max_length=300,
    )

    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)

    bio = models.TextField(blank=True, null=True)

    objects = UserProfileManager()

    def __str__(self):
        return self.username

    def get_friends(self):
        return self.friends.all()

    def add_friend(self, other_user):
        self.friends.add(other_user)
        other_user.friends.add(self)

    def remove_friend(self, other_user):
        self.friends.remove(other_user)
        other_user.friends.remove(self)

    def get_users_not_in_friends(self, obj):
        all_profiles = obj.objects.exclude(id=self.id)
        not_friend_profiles = all_profiles.exclude(id__in=self.friends.values_list('id', flat=True))
        return not_friend_profiles


class Friendship(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='friendships')
    friend = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='friends_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'friend')

    def __str__(self):
        return f"{self.user} is friends with {self.friend}"
