from django.db import models
from django.contrib.auth import get_user_model

class Category(models.Model):
    """
    Represents a category for transactions, associated with a specific user.
    """
    class CategoryType(models.TextChoices):
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

    def __str__(self):
        return self.name