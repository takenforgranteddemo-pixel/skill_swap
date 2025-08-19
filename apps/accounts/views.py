from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User as AuthUser


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # set username (example: from email before '@')
            base_username = user.personal_email.split("@")[0]
            username_candidate = base_username
            from .models import User as ProfileUser
            suffix = 1
            while ProfileUser.objects.filter(username=username_candidate).exists():
                username_candidate = f"{base_username}{suffix}"
                suffix += 1
            user.username = username_candidate
            # set hashed password
            raw_password = form.cleaned_data.get("password")
            user.set_password(raw_password)
            user.save()
            # Create corresponding Django auth user for login
            if not AuthUser.objects.filter(username=user.username).exists():
                auth_user = AuthUser(
                    username=user.username,
                    email=user.personal_email,
                    first_name=user.first_name,
                    last_name=user.last_name,
                )
                auth_user.set_password(raw_password)
                auth_user.save()
            messages.success(request, "Registration successful. Please log in.")
            return redirect("accounts:login")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username", "").strip()
        password = request.POST.get("password", "").strip()
        errors = {}

        # --- VALIDATIONS ---
        if not username:
            errors["username"] = "Username is required."

        if not password:
            errors["password"] = "Password is required."

        if not errors:
            # Try to authenticate user
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Login successful!")
                return redirect('core:home')   # redirect to homepage
            else:
                errors["invalid"] = "Invalid username or password."

        # If errors, re-render login form
        return render(request, 'accounts/login.html', {
            "errors": errors,
            "old_data": request.POST
        })

    return render(request, 'accounts/login.html')

def logout_view(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:home") 