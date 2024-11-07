from PartyHub_Project.Accounts.managers import UserProfileManager
from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.


class UserProfile(AbstractUser):
    points = models.PositiveIntegerField(default=0)

    is_vip = models.BooleanField(default=False)

    followers = models.ManyToManyField(
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

    def get_followers(self):
        return self.follower_set.all()

    def get_following(self):
        return self.following.all()

    def follow(self, other_user):
        if not self.is_following(other_user):
            FollowTable.objects.create(user=self, following=other_user)

    def unfollow(self, other_user):
        FollowTable.objects.filter(user=self, following=other_user).delete()

    def is_following(self, other_user):
        return FollowTable.objects.filter(user=self, following=other_user).exists()

    def get_users_not_in_followers(self):
        return UserProfile.objects.exclude(id=self.id).exclude(id__in=self.get_following().values_list('id', flat=True))


class FollowTable(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following')  # Предотвратява дублиращи записи

    def __str__(self):
        return f"{self.user} is following {self.following}"
