from django.test import TestCase
from django.contrib.auth import get_user_model
from PartyHub_Project.Party.forms import PartyCreateForm, PartyEditForm
from PartyHub_Project.Party.models import Party
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class PartyFormTestsBase(TestCase):
    def setUp(self):
        # Създаваме потребител
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@example.com',
            password='password123',
        )

        # Основни данни за парти
        self.form_data = {
            'title': 'Test Party',
            'description': 'This is a test party.',
            'start_time': timezone.now() + timedelta(days=2),
            'end_time': timezone.now() + timedelta(days=2, hours=4),
            'registration_deadline': timezone.now() + timedelta(days=1),
            'location': 'Test Location',
            'available_spots': 50,
            'party_type': 'disco',
            'is_public': True,
        }


class PartyCreateFormTests(PartyFormTestsBase):
    def test_valid_data(self):
        form = PartyCreateForm(data=self.form_data)
        form.instance.organizer = self.user  # Свързваме с организатор
        self.assertTrue(form.is_valid())

    def test_conflicting_party_times(self):
        # Създаваме съществуващо парти
        Party.objects.create(
            title='Existing Party',
            description='A conflicting party.',
            start_time=timezone.now() + timedelta(days=2, hours=1),
            end_time=timezone.now() + timedelta(days=2, hours=5),
            location='Existing Location',
            available_spots=30,
            party_type='disco',
            is_public=False,
            organizer=self.user,  # Задаваме организатора
        )

        # Добавяме organizer в form_data
        form = PartyCreateForm(data=self.form_data)
        form.instance.organizer = self.user

        self.assertFalse(form.is_valid())
        self.assertIn('__all__', form.errors)


class PartyEditFormTests(PartyFormTestsBase):
    def setUp(self):
        super().setUp()
        # Създаваме първоначално парти
        self.party = Party.objects.create(
            title='Initial Party',
            description='An initial party description.',
            start_time=self.form_data['start_time'],
            end_time=self.form_data['end_time'],
            location=self.form_data['location'],
            available_spots=self.form_data['available_spots'],
            party_type='Private',
            is_public=False,
            organizer=self.user,
        )

    def test_valid_edit(self):
        form = PartyEditForm(instance=self.party, data=self.form_data)
        self.assertTrue(form.is_valid())

    def test_title_already_exists(self):
        Party.objects.create(
            title='Existing Title',
            description='Another party.',
            start_time=timezone.now() + timedelta(days=3),
            end_time=timezone.now() + timedelta(days=3, hours=4),
            location='Another Hall',
            available_spots=30,
            party_type='Public',
            is_public=True,
            organizer=self.user,
        )

        self.form_data['title'] = 'Existing Title'

        form = PartyEditForm(instance=self.party, data=self.form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)

