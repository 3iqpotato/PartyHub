from PartyHub_Project.Party.models import Party
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model


class PartyModelTest(TestCase):

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",email="testemail@email.com", password="password123"
        )
        self.past_time = timezone.now() - timezone.timedelta(days=1)
        self.future_time = timezone.now() + timezone.timedelta(days=2)
        self.base_data = {
            'organizer': self.user,
            "title": "Тестово парти",
            "description": "Описание на партито.",
            "start_time": self.future_time,
            "end_time": self.future_time + timezone.timedelta(hours=2),
            "location": "София, България",
            "party_type": "birthday",
            "available_spots": 10,
        }

    def test_slug_generation(self):
        party = Party.objects.create(**self.base_data)
        self.assertEqual(party.slug, "testovo-parti")

    def test_title_uniqueness(self):
        Party.objects.create(**self.base_data)
        with self.assertRaises(ValidationError):
            duplicate_party = Party(**self.base_data)
            duplicate_party.full_clean()

