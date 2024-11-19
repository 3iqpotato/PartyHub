from django.contrib.auth.models import UserManager
from django.utils import timezone


class UserProfileManager(UserManager):
    def get_users_not_following_user(self, user):
        return self.exclude(id=user.id).exclude(
            id__in=user.get_following().values_list('following_id', flat=True)
        )

    @staticmethod
    def get_user_live_party(user):
        now = timezone.now()
        return user.organized_parties.filter(start_time__lte=now, end_time__gte=now).first()

    @staticmethod
    def get_user_not_started_parties(user):
        now = timezone.now()
        return user.organized_parties.filter(start_time__gte=now)

    def get_user_followers(self, user):
        followers = self.filter(following__following=user)
        return followers

    def get_user_following(self, user):
        return self.filter(follower_set__user=user)

    def get_user_friends(self, user):
        user_followers_list = self.get_user_followers(user)
        friends = user_followers_list.filter(follower_set__user=user)
        return friends
