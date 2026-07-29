from django import forms
from .models import Project
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = [
            'project_code',
            'name',
            'client',
            'description',
            'location',
            'manager',
            'budget',
            'status',
            'start_date',
            'end_date',
        ]

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        if start_date and end_date and end_date < start_date:
            raise forms.ValidationError(
                "End date cannot be earlier than the start date."
            )

        return cleaned_data