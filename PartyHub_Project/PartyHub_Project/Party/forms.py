from PartyHub_Project.Party.models import Party
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import DateTimeInput, TextInput, Select, CheckboxInput



class PartyCreateForm(forms.ModelForm):
    class Meta:
        model = Party
        fields = ['title', 'description', 'date', 'end_date', 'location',
                  'available_spots', 'party_type', 'picture', 'registration_deadline', 'is_public']

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
            'is_public': CheckboxInput(attrs={
                'class': 'form-control',
            })
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Party.objects.filter(title=title).exists():
            raise forms.ValidationError("An event with this title already exists.")

        return title

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("date")
        end_date = cleaned_data.get("end_date")
            # Проверка за конфликти с други партита
        conflicting_parties = Party.objects.filter(
                # Условие 1: Съществуващо парти започва преди края на новото и свършва след началото на новото
                Q(date__lt=end_date, end_date__gt=start_date) |
                # Условие 2: Съществуващо парти започва преди началото на новото и свършва след началото на новото
                Q(date__lt=start_date, end_date__gt=start_date) |
                # Условие 3: Съществуващо парти свършва след началото на новото и започва преди края на новото
                Q(end_date__gt=start_date, date__lt=end_date)
            )

        # .exclude(id=self.id))  # Изключваме текущото парти, ако редактираме // TODO ako pravq forma za editvane da dobavq towa!!!


        if conflicting_parties.exists():
            raise ValidationError("There is another party scheduled during this time. Please choose a different time period.")

        return cleaned_data


