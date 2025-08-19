from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegistrationForm, UserLoginForm
from .models import User
from django.contrib.auth import authenticate, login , logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


def register(request):
    if request.method == "POST":
        # Handle AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = UserRegistrationForm(request.POST, request.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                # set username (example: from email before '@')
                user.username = user.personal_email.split("@")[0]
                # set hashed password
                user.set_password(form.cleaned_data['password'])
                user.save()
                return JsonResponse({
                    'success': True,
                    'message': 'Registration successful! Please login with your credentials.',
                    'redirect_url': '/accounts/login/'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
        
        # Handle regular form submission
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            # set username (example: from email before '@')
            user.username = user.personal_email.split("@")[0]
            # set hashed password
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Registration successful! Please login with your credentials.")
            return redirect("accounts:login")
    else:
        form = UserRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        # Handle AJAX request
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            form = UserLoginForm(request.POST)
            if form.is_valid():
                email = form.cleaned_data['email']
                password = form.cleaned_data['password']
                remember_me = form.cleaned_data['remember_me']
                
                try:
                    user = User.objects.get(personal_email=email)
                    if user.check_password(password):
                        # Simulate Django login (you might need to adjust this based on your authentication backend)
                        request.session['user_id'] = user.id
                        if remember_me:
                            request.session.set_expiry(1209600)  # 2 weeks
                        else:
                            request.session.set_expiry(0)  # Browser session
                        
                        return JsonResponse({
                            'success': True,
                            'message': 'Login successful!',
                            'redirect_url': '/'
                        })
                    else:
                        return JsonResponse({
                            'success': False,
                            'errors': {'__all__': ['Invalid email or password.']}
                        })
                except User.DoesNotExist:
                    return JsonResponse({
                        'success': False,
                        'errors': {'__all__': ['Invalid email or password.']}
                    })
            else:
                return JsonResponse({
                    'success': False,
                    'errors': form.errors
                })
        
        # Handle regular form submission
        form = UserLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']
            
            try:
                user = User.objects.get(personal_email=email)
                if user.check_password(password):
                    # Simulate Django login
                    request.session['user_id'] = user.id
                    if remember_me:
                        request.session.set_expiry(1209600)  # 2 weeks
                    else:
                        request.session.set_expiry(0)  # Browser session
                    
                    messages.success(request, "Login successful!")
                    return redirect('core:home')
                else:
                    messages.error(request, "Invalid email or password.")
            except User.DoesNotExist:
                messages.error(request, "Invalid email or password.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)  
    messages.success(request, "You have been logged out successfully.")
    return redirect("core:home")


def get_branches(request):
    """AJAX endpoint to get branches based on selected department"""
    department_id = request.GET.get('department_id')
    branches = []
    
    if department_id:
        from apps.university.models import Branch
        branches_queryset = Branch.objects.filter(department_id=department_id)
        branches = [{'id': branch.id, 'name': branch.name} for branch in branches_queryset]
    
    return JsonResponse({'branches': branches}) 