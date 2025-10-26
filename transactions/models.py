from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models

from accounts.models import Account
from categories.models import Category


class Transaction(models.Model):
    '''
    Financial transaction model linking accounts and categories.

    Transactions represent financial movements (income or expense) that
    automatically update account balances through signals. Each transaction
    must be associated with an account and category owned by the same user.

    Attributes:
        account: ForeignKey to Account (PROTECT on delete - cannot delete account with transactions)
        category: ForeignKey to Category (PROTECT on delete - cannot delete category with transactions)
        transaction_type: Type of transaction (INCOME or EXPENSE)
        amount: Transaction amount in BRL (must be positive, min 0.01)
        transaction_date: Date when the transaction occurred
        description: Optional text description
        created_at: Timestamp when transaction was created (auto-generated)
        updated_at: Timestamp when transaction was last modified (auto-updated)

    Relationships:
        - Many-to-one with Account via account field
        - Many-to-one with Category via category field
        - Related names: account.transactions, category.transactions

    Balance Updates (Automatic via Signals):
        - CREATE: Adds to balance if INCOME, subtracts if EXPENSE
        - UPDATE: Reverses old transaction, applies new values
        - DELETE: Reverses the transaction effect on balance
        See transactions/signals.py for implementation details

    Validation:
        - transaction_type must match category.category_type
        - amount must be positive (>= 0.01)
        - transaction_date cannot be in the future (form validation)

    Security:
        All queries MUST filter by account__user=request.user to ensure data isolation

    Example:
        transaction = Transaction.objects.create(
            account=user_account,
            category=food_category,
            transaction_type=Transaction.TransactionType.EXPENSE,
            amount=Decimal('50.00'),
            transaction_date=date.today(),
            description='Almoço no restaurante'
        )
    '''

    class TransactionType(models.TextChoices):
        '''Enum for transaction types: INCOME for income, EXPENSE for expenses.'''
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
