from django.contrib import admin

from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """
    Admin configuration for Profile model.

    Displays user email, full name, and phone with search and filter capabilities.
    """

    list_display = (
        'user_email',
        'full_name',
        'phone',
        'created_at',
        'updated_at',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

    search_fields = (
        'user__email',
        'user__username',
        'full_name',
        'phone',
    )

    readonly_fields = (
        'created_at',
        'updated_at',
    )

    fieldsets = (
        ('Informações do Usuário', {
            'fields': ('user',)
        }),
        ('Dados Pessoais', {
            'fields': ('full_name', 'phone')
        }),
        ('Metadados', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    ordering = ('-created_at',)

    def user_email(self, obj):
        """Display the user's email in list view."""
        return obj.user.email if hasattr(obj.user, 'email') else obj.user.username

    user_email.short_description = 'Email'
    user_email.admin_order_field = 'user__email'
