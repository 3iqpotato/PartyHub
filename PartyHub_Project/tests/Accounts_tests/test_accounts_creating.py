from django.test import TestCase
from django.contrib.auth import get_user_model
from PartyHub_Project.Accounts.forms import UserProfileCreateForm

UserProfile = get_user_model()


class UserProfileTests(TestCase):

    def setUp(self):
        self.existing_user = UserProfile.objects.create_user(
            username="existing_user",
            email="existing@example.com",
            password="password123"
        )

    def test_create_user_without_email(self):
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
