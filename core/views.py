"""
Core views for the Finanpy application.
"""
from django.contrib import messages
from django.shortcuts import redirect
from django.views.generic import TemplateView


class HomeView(TemplateView):
    """
    Public home page view for non-authenticated users.

    Displays welcome message, feature highlights, and CTA buttons.
    Authenticated users are automatically redirected to their profile page.
    """

    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        """
        Override get method to redirect authenticated users.

        If user is logged in, redirects to dashboard.
        Non-authenticated users see the public home page.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HttpResponseRedirect: Redirect to dashboard if authenticated
            HttpResponse: Rendered home template if not authenticated
        """
        # Redirect authenticated users to dashboard
        if request.user.is_authenticated:
            return redirect('dashboard')

        # Add test messages to verify the message system works
        if request.GET.get('test_messages'):
            messages.success(request, 'This is a success message!')
            messages.error(request, 'This is an error message!')
            messages.warning(request, 'This is a warning message!')
            messages.info(request, 'This is an info message!')

        return super().get(request, *args, **kwargs)


def page_not_found_view(request, exception):
    """
    Custom 404 error handler.
    """
    return render(request, '404.html', status=404)


def server_error_view(request):
    """
    Custom 500 error handler.
    """
    return render(request, '500.html', status=500)
