'''
Signal handlers for category management.

This module automatically creates default transaction categories when a new
user registers. This provides a better onboarding experience by giving users
a starter set of categories.
'''
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Category

User = get_user_model()


@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    '''
    Signal handler: Create default categories for new users.

    Automatically creates a predefined set of income and expense categories
    when a new user is created. This provides users with commonly used
    categories out of the box, improving the initial user experience.

    Categories Created:
        Income (3 categories):
            - Salário (green)
            - Investimentos (lime)
            - Outras Entradas (emerald)

        Expense (8 categories):
            - Alimentação (red)
            - Transporte (orange)
            - Moradia (blue)
            - Saúde (pink)
            - Lazer (purple)
            - Educação (indigo)
            - Compras (amber)
            - Outras Saídas (gray)

    Args:
        sender: The User model class
        instance: The User instance being saved
        created: Boolean indicating if this is a new user
        **kwargs: Additional signal arguments

    Note:
        Only runs when a new user is created (created=True).
        Users can later modify or delete these categories as needed.
    '''
    if created:
        # Define default categories with colors matching TailwindCSS palette
        default_categories = [
            # Income categories (green tones)
            {'name': 'Salário', 'category_type': 'INCOME', 'color': '#10B981'},
            {'name': 'Investimentos', 'category_type': 'INCOME', 'color': '#84CC16'},
            {'name': 'Outras Entradas', 'category_type': 'INCOME', 'color': '#22C55E'},

            # Expense categories (various colors for visual distinction)
            {'name': 'Alimentação', 'category_type': 'EXPENSE', 'color': '#EF4444'},
            {'name': 'Transporte', 'category_type': 'EXPENSE', 'color': '#F97316'},
            {'name': 'Moradia', 'category_type': 'EXPENSE', 'color': '#3B82F6'},
            {'name': 'Saúde', 'category_type': 'EXPENSE', 'color': '#EC4899'},
            {'name': 'Lazer', 'category_type': 'EXPENSE', 'color': '#A855F7'},
            {'name': 'Educação', 'category_type': 'EXPENSE', 'color': '#6366F1'},
            {'name': 'Compras', 'category_type': 'EXPENSE', 'color': '#F59E0B'},
            {'name': 'Outras Saídas', 'category_type': 'EXPENSE', 'color': '#6B7280'},
        ]

        # Bulk create all categories for the new user
        for category in default_categories:
            Category.objects.create(
                user=instance,
                name=category['name'],
                category_type=category['category_type'],
                color=category['color']
            )
