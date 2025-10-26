from django.contrib import admin

from .models import Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Category model.
    """
    list_display = ('name', 'user', 'category_type', 'color', 'created_at')
    list_filter = ('category_type', 'user')
    search_fields = ('name', 'user__email')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (None, {
            'fields': ('name', 'user', 'category_type', 'color')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        })
    )
