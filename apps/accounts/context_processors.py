from .forms import UserRegistrationForm


def registration_form(request):
    """Provide a blank registration form to all templates for modals."""
    return {
        "registration_form": UserRegistrationForm()
    }

