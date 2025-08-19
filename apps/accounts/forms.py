from django import forms
from .models import User
from apps.university.models import University, Department, Branch

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Password",
            "required": True,
            "autocomplete": "new-password",
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Confirm Password",
            "required": True,
            "autocomplete": "new-password",
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
                "placeholder": "First Name",
                "required": True,
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Last Name",
                "required": True,
            }),
            "gender": forms.RadioSelect(attrs={
                "class": "form-check-input",
                "required": True,
            }),
            "profile_pic": forms.FileInput(attrs={
                "class": "form-control form-control-lg",
            }),
            "university_name": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True,
            }),
            "personal_email": forms.EmailInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Personal Email",
                "required": True,
                "autocomplete": "email",
            }),
            "department": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True,
            }),
            "branch": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True,
            }),
            "year": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True,
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control form-control-lg",
                "rows": 3,
                "placeholder": "Enter your bio",
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Ensure dropdowns are populated from DB and have a friendly empty label
        self.fields["university_name"].queryset = University.objects.all().order_by("name")
        self.fields["department"].queryset = Department.objects.all().order_by("name")
        self.fields["branch"].queryset = Branch.objects.select_related("department").all().order_by("name")
        self.fields["university_name"].empty_label = "Select University"
        self.fields["department"].empty_label = "Select Department"
        self.fields["branch"].empty_label = "Select Branch"

        # Make fields required at the form level regardless of model nullability
        for required_field_name in [
            "first_name",
            "last_name",
            "gender",
            "university_name",
            "personal_email",
            "department",
            "branch",
            "year",
            "password",
            "confirm_password",
        ]:
            if required_field_name in self.fields:
                self.fields[required_field_name].required = True

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        department = cleaned_data.get("department")
        branch = cleaned_data.get("branch")
        profile_pic = cleaned_data.get("profile_pic")

        # Password confirmation
        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        # Ensure branch belongs to selected department
        if branch and department and branch.department_id != department.id:
            self.add_error("branch", "Selected branch does not belong to the chosen department.")

        # Validate image size (max ~2MB)
        if profile_pic and getattr(profile_pic, "size", 0) > 2 * 1024 * 1024:
            self.add_error("profile_pic", "Profile picture must be less than 2MB.")

        return cleaned_data
