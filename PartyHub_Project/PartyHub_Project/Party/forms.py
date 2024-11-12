from PartyHub_Project.Party.models import Party
from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.forms import DateTimeInput, TextInput, Select, CheckboxInput


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

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #
    #     # Пример за добавяне на атрибути за полетата
    #     self.fields['title'].widget.attrs.update({'placeholder': 'Enter party title', 'class': 'form-control'})
    #     self.fields['description'].widget.attrs.update(
    #         {'placeholder': 'Enter event description', 'class': 'form-control', 'rows': 3})
    #     self.fields['date'].widget.attrs.update({'type': 'datetime-local', 'class': 'form-control'})
    #     self.fields['location'].widget.attrs.update({'placeholder': 'Enter location', 'class': 'form-control'})
    #     self.fields['party_type'].widget.attrs.update({'class': 'form-control'})
    #     self.fields['available_spots'].widget.attrs.update({'class': 'form-control', 'min': 2})
    #     self.fields['picture'].widget.attrs.update({'class': 'form-control-file'})
    #     self.fields['registration_deadline'].widget.attrs.update({'type': 'datetime-local', 'class': 'form-control'})
    #     self.fields['end_date'].widget.attrs.update({'type': 'datetime-local', 'class': 'form-control'})
    #     self.fields['is_public'].widget.attrs.update({'class': 'form-control'})



class PartyCreateForm(PartyBaseForm):
    class Meta(PartyBaseForm.Meta):
        pass

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_time")
        end_date = cleaned_data.get("end_time")
            # Проверка за конфликти с други партита
        conflicting_parties = Party.objects.filter(
                # Условие 1: Съществуващо парти започва преди края на новото и свършва след началото на новото
                Q(start_time__lt=end_date, end_time__gt=start_date) |
                # Условие 2: Съществуващо парти започва преди началото на новото и свършва след началото на новото
                Q(start_time__lt=start_date, end_time__gt=start_date) |
                # Условие 3: Съществуващо парти свършва след началото на новото и започва преди края на новото
                Q(end_time__gt=start_date, start_time__lt=end_date)
            )

        # .exclude(id=self.id))  # Изключваме текущото парти, ако редактираме // TODO ako pravq forma za editvane da dobavq towa!!!

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
        fields = ['title', 'description', 'location', 'party_type', 'picture']

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if Party.objects.exclude(id=self.instance.id).filter(title=title).exists():
            raise forms.ValidationError("An event with this title already exists.")
        return title