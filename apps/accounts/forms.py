from django import forms
from .models import User
from apps.university.models import Branch

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

    def clean_personal_email(self):
        email = self.cleaned_data.get("personal_email", "").strip().lower()
        if not email:
            raise forms.ValidationError("Personal email is required.")
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password", "")
        if len(password) < 8:
            raise forms.ValidationError("Password must be at least 8 characters long.")
        return password

    def clean(self):
        cleaned = super().clean()
        department = cleaned.get("department")
        branch = cleaned.get("branch")
        year = cleaned.get("year")

        if department and branch:
            if not Branch.objects.filter(id=branch.id, department=department).exists():
                self.add_error("branch", "Selected branch does not belong to the selected department.")

        valid_year_values = {choice[0] for choice in User.YEAR_CHOCIES}
        if year and year not in valid_year_values:
            self.add_error("year", "Invalid year selection.")

        return cleaned
