from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from PartyHub_Project.Party.models import Party

class LivePartyAccessTest(TestCase):

    def setUp(self):
        self.organizer = get_user_model().objects.create_user(username="organizer",email='testemail1', password="testpassword")
        self.participant = get_user_model().objects.create_user(username="participant",email='testemail2', password="testpassword")

        self.party = Party.objects.create(
            organizer=self.organizer,
            title="Live Party",
            start_time=timezone.now() - timedelta(hours=1),
            end_time=timezone.now() + timedelta(hours=1),
            slug="live-party",
            location = "София, България",
            party_type = "birthday",
            available_spots = 10,
        )

    def test_access_as_organizer(self):
        self.client.login(username="organizer",email='testemail3', password="testpassword")
        response = self.client.get(reverse('live_party', kwargs={'slug': self.party.slug}))
        self.assertEqual(response.status_code, 200)

    def test_access_as_participant(self):
        self.client.login(username="participant",email='testemail4', password="testpassword")
        response = self.client.get(reverse('live_party', kwargs={'slug': self.party.slug}))
        self.assertEqual(response.status_code, 403)

    def test_access_without_login(self):
        response = self.client.get(reverse('live_party', kwargs={'slug': self.party.slug}))
        self.assertRedirects(response, '/accounts/login/?next=/parties/live_party/live-party')
