"""
Core views for the Finanpy application.
"""
from django.shortcuts import render
from django.contrib import messages


def home(request):
    """
    Home page view - displays welcome message and basic info.
    """
    # Add test messages to verify the message system works
    if request.GET.get('test_messages'):
        messages.success(request, 'This is a success message!')
        messages.error(request, 'This is an error message!')
        messages.warning(request, 'This is a warning message!')
        messages.info(request, 'This is an info message!')

    return render(request, 'home.html')
