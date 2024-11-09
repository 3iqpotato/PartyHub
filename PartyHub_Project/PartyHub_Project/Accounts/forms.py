from PartyHub_Project.Accounts.mixins import RemoveHelpTextMixin
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model


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

    # def clean_email(self):
    #     email = self.cleaned_data.get('email')
    #     if get_user_model().objects.filter(email=email).exists():
    #         raise forms.ValidationError("This email is already in use.")
    #     return email



class UserProfileLoginForm(RemoveHelpTextMixin, AuthenticationForm):
    username = forms.CharField(
        label="Username or email ",
        widget=forms.TextInput(attrs={'placeholder': 'Enter your username or email...'}),
    )

