from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import Account
from categories.models import Category


class Transaction(models.Model):
    """
    Represents a financial transaction belonging to a user's account.

    Transactions can be of type income or expense and are associated with
    both an account and a category owned by the user.
    """

    class TransactionType(models.TextChoices):
        INCOME = 'INCOME', 'Entrada'
        EXPENSE = 'EXPENSE', 'Saída'

    account = models.ForeignKey(
        Account,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Conta'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='transactions',
        verbose_name='Categoria'
    )
    transaction_type = models.CharField(
        max_length=7,
        choices=TransactionType.choices,
        verbose_name='Tipo'
    )
    amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name='Valor'
    )
    transaction_date = models.DateField(
        verbose_name='Data da Transação'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        verbose_name = 'Transação'
        verbose_name_plural = 'Transações'
        ordering = ['-transaction_date', '-created_at']
        indexes = [
            models.Index(fields=['account', '-transaction_date']),
            models.Index(fields=['category', 'transaction_type']),
        ]

    def __str__(self):
        """
        Return a human readable representation of the transaction.
        """
        type_display = self.get_transaction_type_display()
        return f'{type_display} - {self.account.name} ({self.amount})'
