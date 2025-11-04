"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.urls import include, path

from core import views as core_views
from core.views import HomeView
from users.views import DashboardView

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('admin/', admin.site.urls),
    path('auth/', include('users.urls')),
    path('profile/', include('profiles.urls')),
    path('accounts/', include('accounts.urls', namespace='accounts')),
    path('categories/', include('categories.urls', namespace='categories')),
    path('transactions/', include('transactions.urls', namespace='transactions')),
]

# Include debug toolbar URLs only in development when DEBUG is True
if settings.DEBUG:
    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

handler404 = core_views.page_not_found_view
handler500 = core_views.server_error_view
