from PartyHub_Project.Party.models import Party
from django import forms
from django.forms import DateTimeInput, TextInput, Select
from django.utils import timezone


class PartyCreateForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['title', 'description', 'date', 'end_date', 'location',
                  'available_spots', 'party_type', 'picture', 'registration_deadline']

        widgets = {
            'title': TextInput(attrs={
                'placeholder': 'Enter party title',
                'class': 'form-control',
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Enter event description',
                'class': 'form-control',
                'rows': 3
            }),
            'date': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'location': TextInput(attrs={
                'placeholder': 'Enter location',
                'class': 'form-control',
            }),
            'party_type': Select(attrs={
                'class': 'form-control',
            }),
            'available_spots': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 2,
            }),
            'picture': forms.ClearableFileInput(attrs={
                'class': 'form-control-file',
            }),
            'registration_deadline': DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
            'end_date':  DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'form-control',
            }),
        }

        def clean_title(self):
            title = self.cleaned_data.get('title')
            if Party.objects.filter(title=title).exists():
                raise forms.ValidationError("An event with this title already exists.")
            return title
