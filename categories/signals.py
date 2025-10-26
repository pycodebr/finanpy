from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Category

User = get_user_model()

@receiver(post_save, sender=User)
def create_default_categories(sender, instance, created, **kwargs):
    if created:
        default_categories = [
            # Entradas
            {'name': 'Salário', 'category_type': 'INCOME', 'color': '#10B981'},
            {'name': 'Investimentos', 'category_type': 'INCOME', 'color': '#84CC16'},
            {'name': 'Outras Entradas', 'category_type': 'INCOME', 'color': '#22C55E'},

            # Saídas
            {'name': 'Alimentação', 'category_type': 'EXPENSE', 'color': '#EF4444'},
            {'name': 'Transporte', 'category_type': 'EXPENSE', 'color': '#F97316'},
            {'name': 'Moradia', 'category_type': 'EXPENSE', 'color': '#3B82F6'},
            {'name': 'Saúde', 'category_type': 'EXPENSE', 'color': '#EC4899'},
            {'name': 'Lazer', 'category_type': 'EXPENSE', 'color': '#A855F7'},
            {'name': 'Educação', 'category_type': 'EXPENSE', 'color': '#6366F1'},
            {'name': 'Compras', 'category_type': 'EXPENSE', 'color': '#F59E0B'},
            {'name': 'Outras Saídas', 'category_type': 'EXPENSE', 'color': '#6B7280'},
        ]

        for category in default_categories:
            Category.objects.create(
                user=instance,
                name=category['name'],
                category_type=category['category_type'],
                color=category['color']
            )
