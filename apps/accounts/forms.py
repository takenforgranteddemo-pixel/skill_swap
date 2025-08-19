from django import forms
from .models import User

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Password"
        })
    )

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "gender",
            "profile_pic",
            "university_name",
            "personal_email",
            "department",
            "branch",
            "year",
            "bio",
        ]

        widgets = {
            "first_name": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "First Name"
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Last Name"
            }),
            "gender": forms.RadioSelect(attrs={
                "class": "form-check-input"
            }),
            "profile_pic": forms.FileInput(attrs={
                "class": "form-control form-control-lg"
            }),
            "university_name": forms.Select(attrs={
                "class": "form-select form-select-lg"
            }),
            "personal_email": forms.EmailInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Personal Email"
            }),
            "department": forms.Select(attrs={
                "class": "form-select form-select-lg"
            }),
            "branch": forms.Select(attrs={
                "class": "form-select form-select-lg"
            }),
            "year": forms.Select(attrs={
                "class": "form-select form-select-lg"
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control form-control-lg",
                "rows": 3,
                "placeholder": "Enter your bio"
            }),
        }
