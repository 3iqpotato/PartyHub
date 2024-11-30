# Във файл: party_app/serializers.py
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Party

UserModel = get_user_model()


class UserInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = ['username']


class PartySerializer(serializers.ModelSerializer):
    organizer = UserInfoSerializer(read_only=True)  # no one can touch it with his dirty little hands
    class Meta:
        model = Party
        fields = ['title', 'organizer', 'start_time', 'description']