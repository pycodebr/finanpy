from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """
    Admin configuration for Transaction model.
    """

    list_display = (
        'transaction_date',
        'description',
        'account',
        'category',
        'transaction_type',
        'amount',
    )
    list_filter = (
        'transaction_type',
        'transaction_date',
        'category',
    )
    search_fields = (
        'description',
        'account__name',
    )
    date_hierarchy = 'transaction_date'
    readonly_fields = (
        'created_at',
        'updated_at',
    )
    list_select_related = (
        'account',
        'category',
    )
    ordering = ('-transaction_date', '-created_at')
