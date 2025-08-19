from django import forms
from .models import User
from apps.university.models import University, Department, Branch
import re

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        min_length=8,
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Password (min 8 characters)",
            "required": True
        }),
        help_text="Password must be at least 8 characters long"
    )
    
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Confirm Password",
            "required": True
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
                "required": True
            }),
            "last_name": forms.TextInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Last Name",
                "required": True
            }),
            "gender": forms.RadioSelect(attrs={
                "class": "form-check-input"
            }),
            "profile_pic": forms.FileInput(attrs={
                "class": "form-control form-control-lg",
                "accept": "image/*"
            }),
            "university_name": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True
            }),
            "personal_email": forms.EmailInput(attrs={
                "class": "form-control form-control-lg",
                "placeholder": "Personal Email",
                "required": True
            }),
            "department": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True
            }),
            "branch": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True
            }),
            "year": forms.Select(attrs={
                "class": "form-select form-select-lg",
                "required": True
            }),
            "bio": forms.Textarea(attrs={
                "class": "form-control form-control-lg",
                "rows": 3,
                "placeholder": "Enter your bio (optional)",
                "maxlength": "250"
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Populate university dropdown with database values
        self.fields['university_name'].queryset = University.objects.all()
        self.fields['university_name'].empty_label = "Select University"
        
        # Populate department dropdown with database values
        self.fields['department'].queryset = Department.objects.all()
        self.fields['department'].empty_label = "Select Department"
        
        # Populate branch dropdown with database values
        self.fields['branch'].queryset = Branch.objects.all()
        self.fields['branch'].empty_label = "Select Branch"
        
        # Make certain fields required
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['gender'].required = True
        self.fields['university_name'].required = True
        self.fields['personal_email'].required = True
        self.fields['department'].required = True
        self.fields['branch'].required = True
        self.fields['year'].required = True

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name and not re.match(r'^[a-zA-Z\s]+$', first_name):
            raise forms.ValidationError("First name should only contain letters and spaces.")
        if first_name and len(first_name.strip()) < 2:
            raise forms.ValidationError("First name must be at least 2 characters long.")
        return first_name.strip() if first_name else first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if last_name and not re.match(r'^[a-zA-Z\s]+$', last_name):
            raise forms.ValidationError("Last name should only contain letters and spaces.")
        if last_name and len(last_name.strip()) < 2:
            raise forms.ValidationError("Last name must be at least 2 characters long.")
        return last_name.strip() if last_name else last_name

    def clean_personal_email(self):
        email = self.cleaned_data.get('personal_email')
        if email and User.objects.filter(personal_email=email).exists():
            raise forms.ValidationError("This email address is already registered.")
        return email

    def clean_profile_pic(self):
        profile_pic = self.cleaned_data.get('profile_pic')
        if profile_pic:
            # Check file size (max 5MB)
            if profile_pic.size > 5 * 1024 * 1024:
                raise forms.ValidationError("Image file size should not exceed 5MB.")
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/jpg', 'image/png', 'image/gif']
            if profile_pic.content_type not in allowed_types:
                raise forms.ValidationError("Only JPEG, PNG, and GIF images are allowed.")
        return profile_pic

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        
        if password and confirm_password:
            if password != confirm_password:
                raise forms.ValidationError("Passwords do not match.")
        
        return cleaned_data


class UserLoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Enter your email",
            "required": True,
            "id": "loginEmail"
        })
    )
    
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control form-control-lg",
            "placeholder": "Enter your password",
            "required": True,
            "id": "loginPassword"
        })
    )
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            "class": "form-check-input",
            "id": "rememberMe"
        })
    )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and not User.objects.filter(personal_email=email).exists():
            raise forms.ValidationError("No account found with this email address.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        
        if email and password:
            try:
                user = User.objects.get(personal_email=email)
                if not user.check_password(password):
                    raise forms.ValidationError("Invalid email or password.")
            except User.DoesNotExist:
                raise forms.ValidationError("Invalid email or password.")
        
        return cleaned_data
