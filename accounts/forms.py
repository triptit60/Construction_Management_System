from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class SignUpForm(UserCreationForm):
    role = forms.ChoiceField(
        choices=UserProfile.ROLE_CHOICES, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Apply Bootstrap styling to input fields
        for field in self.fields.values():
            if not isinstance(field.widget, forms.Select):
                field.widget.attrs['class'] = 'form-control'

    def save(self, commit=True):
     user = super().save(commit=False)
     user.email = self.cleaned_data["email"]

     if commit:
        user.save()

     return user 