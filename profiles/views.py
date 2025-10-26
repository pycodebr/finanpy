from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView

from .forms import ProfileForm
from .models import Profile


class ProfileDetailView(LoginRequiredMixin, DetailView):
    """
    View to display the profile of the authenticated user.

    Security:
    - LoginRequiredMixin ensures only authenticated users can access
    - get_object override ensures users can only view their own profile
    - No pk parameter needed in URL - always shows current user's profile
    """
    model = Profile
    template_name = 'profiles/profile_detail.html'
    context_object_name = 'profile'

    def get_object(self, queryset=None):
        """
        Override to always return the profile of the authenticated user.

        This ensures:
        1. User cannot access other users' profiles
        2. No need for pk in URL
        3. Simple and secure access pattern

        Returns:
            Profile: The profile instance of the logged-in user
        """
        return self.request.user.profile


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating the profile of the authenticated user.

    Security:
    - LoginRequiredMixin ensures only authenticated users can access
    - get_object override ensures users can only edit their own profile
    - No pk parameter needed in URL - always edits current user's profile
    - Displays success message after successful update
    """
    model = Profile
    form_class = ProfileForm
    template_name = 'profiles/profile_form.html'
    success_url = reverse_lazy('profiles:profile_detail')

    def get_object(self, queryset=None):
        """
        Override to always return the profile of the authenticated user.

        This ensures users can only edit their own profile and prevents
        unauthorized access to other users' profiles.

        Returns:
            Profile: The profile instance of the logged-in user
        """
        return self.request.user.profile

    def form_valid(self, form):
        """
        Display success message after successful profile update.

        Args:
            form: The validated ProfileForm instance

        Returns:
            HttpResponse: Redirect to success_url after saving
        """
        messages.success(self.request, 'Perfil atualizado com sucesso!')
        return super().form_valid(form)
