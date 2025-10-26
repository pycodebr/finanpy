from django.contrib import admin

from .models import Account


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    """
    Admin configuration for Account model.

    Provides a comprehensive interface for managing user accounts with
    filtering, searching, and read-only timestamp fields.
    """

    list_display = [
        'name',
        'user_email',
        'bank_name',
        'account_type',
        'balance',
        'is_active',
    ]

    list_filter = [
        'account_type',
        'is_active',
    ]

    search_fields = [
        'name',
        'bank_name',
        'user__email',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    def user_email(self, obj):
        """Display the user's email address."""
        return obj.user.email

    user_email.short_description = 'Email do Usuário'
    user_email.admin_order_field = 'user__email'
