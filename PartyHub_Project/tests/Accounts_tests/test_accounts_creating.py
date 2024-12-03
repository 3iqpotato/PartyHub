from django.test import TestCase
from django.contrib.auth import get_user_model
from PartyHub_Project.Accounts.forms import UserProfileCreateForm

UserProfile = get_user_model()

class UserProfileTests(TestCase):

    def setUp(self):
        # Създаване на тестов потребител
        self.existing_user = UserProfile.objects.create_user(
            username="existing_user",
            email="existing@example.com",
            password="password123"
        )

    def test_create_user_without_email(self):
        # Формуляр с липсващ имейл
        form_data = {
            "username": "testuser",
            "email": "",
            "password1": "password123",
            "password2": "password123"
        }
        form = UserProfileCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_create_user_without_username(self):
        # Формуляр с липсващо потребителско име
        form_data = {
            "username": "",
            "email": "test@example.com",
            "password1": "password123",
            "password2": "password123"
        }
        form = UserProfileCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_create_user_with_duplicate_email(self):
        # Формуляр с дублиран имейл
        form_data = {
            "username": "newuser",
            "email": "existing@example.com",
            "password1": "password123",
            "password2": "password123"
        }
        form = UserProfileCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_create_user_with_duplicate_username(self):
        # Формуляр с дублирано потребителско име
        form_data = {
            "username": "existing_user",
            "email": "newuser@example.com",
            "password1": "password123",
            "password2": "password123"
        }
        form = UserProfileCreateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("username", form.errors)

    def test_create_user_with_valid_data(self):
        # Формуляр с валидни данни
        form_data = {
            "username": "newuser3",
            "email": "newuser3@example.com",
            "password1": "password123@123",
            "password2": "password123@123"
        }
        form = UserProfileCreateForm(data=form_data)
        self.assertTrue(form.is_valid())

        user = form.save()
        self.assertEqual(user.username, "newuser3")
        self.assertEqual(user.email, "newuser3@example.com")
