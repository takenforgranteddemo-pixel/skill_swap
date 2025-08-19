from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm
from django.contrib.auth import authenticate, login , logout


def register(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # set username (example: from email before '@')
            user.username = user.personal_email.split("@")[0]
            # set hashed password
            user.set_password(form.cleaned_data.get("password"))
            user.save()
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