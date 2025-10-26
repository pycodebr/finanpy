"""
URL configuration for the accounts app.

This module defines URL patterns for managing bank accounts, including:
- List view: Display all user accounts
- Create view: Add a new account
- Update view: Edit an existing account
- Delete view: Remove an account

All views require user authentication and enforce data isolation
(users can only access their own accounts).
"""
from django.urls import path

from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.AccountListView.as_view(), name='account_list'),
    path('new/', views.AccountCreateView.as_view(), name='account_create'),
    path('<int:pk>/edit/', views.AccountUpdateView.as_view(), name='account_update'),
    path('<int:pk>/delete/', views.AccountDeleteView.as_view(), name='account_delete'),
]
