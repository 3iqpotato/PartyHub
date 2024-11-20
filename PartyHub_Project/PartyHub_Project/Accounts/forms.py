from PartyHub_Project.Accounts.mixins import RemoveHelpTextMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model
from django.forms import models


class UserProfileBaseForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileCreateForm(RemoveHelpTextMixin, UserProfileBaseForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username...'}),
    )

    email = forms.CharField(
        label="Email",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your email...'}),
    )

    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password...'}),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Confirm your password...'}),
    )


class UserProfileLoginForm(RemoveHelpTextMixin, AuthenticationForm):
    username = forms.CharField(
        label="Username or email ",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username or email...'}),
    )

    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'Enter your password...'}),
    )


class UserProfileEditForm(RemoveHelpTextMixin, models.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['username', 'first_name', 'last_name', 'profile_picture', 'bio',]

    def clean(self):
        cleaned_data = super().clean()
        if not cleaned_data.get('profile_picture'):
            self.instance.profile_picture = 'profiles/default_img.jpg'
        return cleaned_data
