from django.urls import path
from .views import (
    CategoryListView,
    CategoryCreateView,
    CategoryUpdateView,
    CategoryDeleteView
)

app_name = 'categories'

urlpatterns = [
    path('', CategoryListView.as_view(), name='category_list'),
    path('new/', CategoryCreateView.as_view(), name='category_create'),
    path('<int:pk>/edit/', CategoryUpdateView.as_view(), name='category_update'),
    path('<int:pk>/delete/', CategoryDeleteView.as_view(), name='category_delete'),
]
