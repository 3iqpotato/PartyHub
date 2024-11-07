from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db import models


class UserProfileManager(UserManager):
    # def get_users_not_in_friends(self, user):
    #     non_friends = user.objects.exclude(id=user.id)
    #     # .exclude(
    #     #     id__in=self.friends.values_list('id', flat=True))
    #     # non_friends = all_users.
    #     return non_friends
    pass