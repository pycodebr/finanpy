from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    """Admin configuration for CustomUser model using email authentication."""

    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'is_staff', 'is_active', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'is_superuser']
    search_fields = ['email', 'first_name', 'last_name']
    ordering = ['email']

    # Fieldsets for editing existing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name')}),
        ('Permissões', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined', 'created_at', 'updated_at')}),
    )

    # Fieldsets for adding new users
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active'),
        }),
    )

    # Read-only fields (auto-generated timestamps)
    readonly_fields = ['date_joined', 'last_login', 'created_at', 'updated_at']


admin.site.register(CustomUser, CustomUserAdmin)
