from django.contrib.auth import get_user_model
from django.db import models


class Category(models.Model):
    '''
    Transaction category model for organizing income and expenses.

    Each category belongs to a specific user and has a type (INCOME or EXPENSE).
    Categories are protected from deletion if they have associated transactions
    (PROTECT constraint). Default categories are auto-created for new users via
    signal in categories/signals.py.

    Attributes:
        user: ForeignKey to CustomUser (CASCADE on delete)
        name: Category name (must be unique per user)
        category_type: Type of category (INCOME or EXPENSE)
        color: Hex color code for UI display (default: '#667eea')
        created_at: Timestamp when category was created (auto-generated)
        updated_at: Timestamp when category was last modified (auto-updated)

    Relationships:
        - Many-to-one with CustomUser via user field
        - One-to-many with Transaction via transactions reverse relation
        - Related name: user.categories

    Constraints:
        - unique_together on (user, name) - prevents duplicate category names per user
        - Transactions use PROTECT on delete - cannot delete category with transactions

    Security:
        All queries MUST filter by user=request.user to ensure data isolation

    Example:
        category = Category.objects.create(
            user=request.user,
            name='Alimentação',
            category_type=Category.CategoryType.EXPENSE,
            color='#ef4444'
        )
    '''
    class CategoryType(models.TextChoices):
        '''Enum for category types: INCOME for income, EXPENSE for expenses.'''
        INCOME = 'INCOME', 'Income'
        EXPENSE = 'EXPENSE', 'Expense'

    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='categories'
    )
    name = models.CharField(max_length=50)
    category_type = models.CharField(
        max_length=7,
        choices=CategoryType.choices
    )
    color = models.CharField(max_length=7, default='#667eea')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']
        unique_together = ('user', 'name')
        indexes = [
            models.Index(fields=['user', 'category_type']),
            models.Index(fields=['user', 'name']),
        ]

    def __str__(self):
        '''
        Return string representation of the category.

        Returns:
            str: The category name
        '''
        return self.name
