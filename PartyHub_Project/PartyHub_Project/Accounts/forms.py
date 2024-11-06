from PartyHub_Project.Accounts.mixins import RemoveHelpTextMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import EmailValidator


class UserProfileBaseForm(UserCreationForm):
    username = forms.CharField(
        label="Username or Email",  # Показваме надписа "Username or Email"
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username or email'}),
    )

    class Meta(UserCreationForm.Meta):
        model = get_user_model()  # Use the custom user model

    def clean_username(self):
        """
        Проверяваме дали въведеното е валидно потребителско име или имейл.
        """
        username_or_email = self.cleaned_data.get('username')

        # Проверка дали е валиден имейл
        try:
            EmailValidator()(username_or_email)  # Пробваме да валидираме имейл
            # Ако е валиден имейл, проверяваме дали вече има такъв имейл в базата данни
            if get_user_model().objects.filter(email=username_or_email).exists():
                raise ValidationError("This email is already taken.")
            return username_or_email
        except ValidationError:
            # Ако не е валиден имейл, продължаваме с проверка за потребителско име
            pass

        # Ако не е имейл, ще го приемем като потребителско име и проверим дали съществува
        if get_user_model().objects.filter(username=username_or_email).exists():
            raise ValidationError("This username is already taken.")

        return username_or_email


class UserProfileCreateForm(RemoveHelpTextMixin, UserProfileBaseForm):
    pass
