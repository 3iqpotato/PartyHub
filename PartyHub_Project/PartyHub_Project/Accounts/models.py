from PartyHub_Project.Accounts.managers import UserProfileManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

# Create your models here.


class UserProfile(AbstractUser):
    points = models.PositiveIntegerField(default=0)

    email = models.EmailField(_("email address"), blank=False, null=False, unique=True)

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

    def is_vip(self):
        return self.points > 300

    def get_valid_tickets(self):
        now = timezone.now()
        return self.tickets.filter(party__end_time__gt=now).exclude(checked=True)

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
        all_users = UserProfile.objects.exclude(id=self.id)
        not_following = all_users.exclude(id__in=self.get_following().values_list('following_id', flat=True))
        return not_following

    def get_live_party(self):
        now = timezone.now()
        party = self.organized_parties.filter(start_time__lte=now, end_time__gte=now).first()
        return party

    def get_not_started_parties(self):
        now = timezone.now()
        return self.organized_parties.filter(start_time__gte=now)

    # def get_parties(self):
    #     return self.organized_parties


class FollowTable(models.Model):
    user = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='following')
    following = models.ForeignKey(to=UserProfile, on_delete=models.CASCADE, related_name='follower_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'following')

    def __str__(self):
        return f"{self.user} is following {self.following}"
