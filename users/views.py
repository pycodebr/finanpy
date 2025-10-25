from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from .forms import LoginForm, SignupForm


class LoginView(FormView):
    """
    View for user authentication with custom email-based login.

    Uses LoginForm with email (not username) as the identifier field.
    Validates credentials and logs in the user on success.
    Displays error messages for invalid credentials.
    """

    form_class = LoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """
        Process valid form submission and authenticate user.

        Attempts to authenticate user with provided email and password.
        On success: logs in user, displays success message, and redirects to dashboard.
        On failure: adds error to form and returns to login page.

        Args:
            form: The validated LoginForm instance

        Returns:
            HttpResponseRedirect: Redirect to success_url on valid credentials
            HttpResponse: Rendered form with errors on invalid credentials
        """
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Authenticate using email as username (CustomUser configuration)
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            # Valid credentials - log in user
            login(self.request, user)

            # Display success message
            messages.success(
                self.request,
                f'Bem-vindo de volta, {user.email}!'
            )

            return super().form_valid(form)
        else:
            # Invalid credentials - add error to form
            form.add_error(
                None,
                'Email ou senha incorretos. Por favor, tente novamente.'
            )
            return self.form_invalid(form)


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


class CustomLogoutView(DjangoLogoutView):
    """
    Custom logout view that adds a success message.

    Inherits from Django's LogoutView and overrides dispatch()
    to display a friendly success message before logging out.
    Redirects to LOGOUT_REDIRECT_URL configured in settings.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to add success message before logout.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HttpResponseRedirect: Redirect to LOGOUT_REDIRECT_URL
        """
        messages.success(request, 'Você saiu da sua conta com sucesso. Até logo!')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard view for authenticated users.

    Displays a welcome message and placeholder sections for upcoming features
    (Accounts, Categories, Transactions - to be implemented in Sprints 2-4).

    This is a minimal implementation to fix the authentication redirect issue.
    The dashboard will be enhanced with real data and widgets in Sprint 5.
    """

    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Add user information to the template context.

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            dict: Context dictionary with user information
        """
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user
        return context
