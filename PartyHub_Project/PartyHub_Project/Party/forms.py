from PartyHub_Project.Party.models import Party
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import DateTimeInput, TextInput, Select, CheckboxInput
from django.utils import timezone


class PartyBaseForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['title', 'description', 'start_time', 'end_time', 'location',
                  'available_spots', 'party_type', 'picture', 'registration_deadline', 'is_public']

        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Enter party title',
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter event description',
                'class': 'form-control',
                'rows': 3
            }),
            'start_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Start date and time'
            }),
            'end_time': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'End date and time'
            }),
            'location': forms.TextInput(attrs={
                'placeholder': 'Enter location',
                'class': 'form-control',
            }),
            'party_type': forms.Select(attrs={
                'class': 'form-control',
            }),
            'available_spots': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2,
                'placeholder': 'Enter available spots'
            }),
            'picture': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            'registration_deadline': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
                'placeholder': 'Registration deadline'
            }),
            'is_public': forms.CheckboxInput(attrs={
                'class': 'form-control',
            })
        }


class PartyCreateForm(PartyBaseForm):
    class Meta(PartyBaseForm.Meta):
        pass

    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")
        registration_deadline = cleaned_data.get("registration_deadline")
        organizer = cleaned_data.get("organizer")

        if not start_time or not end_time:
            raise ValidationError("Both start and end times must be provided.")

        if start_time < timezone.now():
            raise ValidationError({"start_time": "The party start cannot be in the past."})

            # Проверка дали края на събитието е след началото
        if end_time <= start_time:
                raise ValidationError({"end_time": "The end time must be after the start time."})

            # Проверка за срок на регистрация
        if registration_deadline and registration_deadline > start_time:
            raise ValidationError(
                    {"registration_deadline": "The registration deadline cannot be after the event date."})

            # Проверка за конфликти с други партита
        conflicting_parties = Party.objects.filter(organizer=organizer).filter(
                # Условие 1: Съществуващо парти започва преди края на новото и свършва след началото на новото
                Q(start_time__lt=end_time, end_time__gt=start_time) |
                # Условие 2: Съществуващо парти започва преди началото на новото и свършва след началото на новото
                Q(start_time__lt=start_time, end_time__gt=start_time) |
                # Условие 3: Съществуващо парти свършва след началото на новото и започва преди края на новото
                Q(end_time__gt=start_time, start_time__lt=end_time)
            )

        if conflicting_parties.exists():
            raise ValidationError("There is another party scheduled during this time. Please choose a different time period.")

        return cleaned_data

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Party.objects.filter(title=title).exists() :
            raise forms.ValidationError("An event with this title already exists.")

        return title


class PartyEditForm(PartyBaseForm):
    class Meta(PartyBaseForm.Meta):
        model = Party
        fields = ['title', 'description', 'location', 'party_type', 'picture', 'available_spots']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Party.objects.exclude(id=self.instance.id).filter(title=title).exists():
            raise forms.ValidationError("An event with this title already exists.")
        return title

    def clean_available_spots(self):
        available_spots = self.cleaned_data.get('available_spots')
        if available_spots is not None:
            current_tickets_sold = self.instance.tickets.count()
            if available_spots < current_tickets_sold:
                raise forms.ValidationError(
                    f"The maximum tickets cannot be less than the number of already sold tickets ({current_tickets_sold})."
                )
        return available_spots