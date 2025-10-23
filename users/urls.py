"""
URL configuration for the users app.

Handles authentication-related routes including signup and login.
"""
from django.urls import path

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
]
