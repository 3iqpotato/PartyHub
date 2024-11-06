from django.apps import apps
from django.contrib import auth
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import UserManager
from django.db import models


class UserProfileManager(UserManager):

    def get_user_with_full_data(self, *args, **kwargs):
        """
        This method optimizes the query by using select_related to fetch the
        user and their associated profile in a single query.
        It reduces the number of queries, improving performance when loading
        many users at once.
        """
        return self.select_related('user').filter(*args, **kwargs)