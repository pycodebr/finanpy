"""
Core views for the Finanpy application.
"""
from django.shortcuts import redirect
from django.views.generic import TemplateView
from django.contrib import messages


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

        If user is logged in, redirects to admin (temporary until dashboard is available).
        Non-authenticated users see the public home page.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HttpResponseRedirect: Redirect to admin if authenticated
            HttpResponse: Rendered home template if not authenticated
        """
        # Redirect authenticated users to admin page
        # TODO: Change to redirect('dashboard') when Task 5.1 is implemented
        if request.user.is_authenticated:
            messages.info(
                request,
                'Bem-vindo! O dashboard está em desenvolvimento. '
                'Por enquanto, você pode acessar o painel administrativo.'
            )
            return redirect('admin:index')

        # Add test messages to verify the message system works
        if request.GET.get('test_messages'):
            messages.success(request, 'This is a success message!')
            messages.error(request, 'This is an error message!')
            messages.warning(request, 'This is a warning message!')
            messages.info(request, 'This is an info message!')

        return super().get(request, *args, **kwargs)
