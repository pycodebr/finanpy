from django.contrib import messages
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import SignupForm


class SignupView(CreateView):
    """
    View for user registration with automatic login after signup.

    Uses SignupForm for custom email-based authentication.
    After successful registration, automatically logs in the user
    and redirects to the dashboard.
    """

    form_class = SignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """
        Process valid form submission.

        Saves the new user, automatically logs them in,
        displays success message, and redirects to dashboard.

        Args:
            form: The validated SignupForm instance

        Returns:
            HttpResponseRedirect: Redirect to success_url (dashboard)
        """
        response = super().form_valid(form)

        # Automatically log in the user after successful registration
        login(self.request, self.object)

        # Display success message
        messages.success(
            self.request,
            f'Bem-vindo ao Finanpy, {self.object.email}! Sua conta foi criada com sucesso.'
        )

        return response
