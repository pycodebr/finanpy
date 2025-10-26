from django.urls import path

from .views import ProfileDetailView, ProfileUpdateView

app_name = 'profiles'

urlpatterns = [
    path('', ProfileDetailView.as_view(), name='profile_detail'),
    path('edit/', ProfileUpdateView.as_view(), name='profile_update'),
]
