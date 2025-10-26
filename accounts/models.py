from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Account(models.Model):
    '''
    Bank account or wallet model for tracking user finances.

    Each account belongs to a specific user and maintains a balance that is
    automatically updated through transaction signals. Accounts support three
    types: checking, savings, and wallet. Deleting an account cascades to all
    associated transactions.

    Attributes:
        user: ForeignKey to CustomUser (CASCADE on delete)
        name: Custom name for the account (e.g., 'Conta Principal')
        bank_name: Name of the financial institution
        account_type: Type of account (CHECKING, SAVINGS, or WALLET)
        balance: Current account balance (auto-updated via signals)
        is_active: Whether the account is currently active
        created_at: Timestamp when account was created (auto-generated)
        updated_at: Timestamp when account was last modified (auto-updated)

    Relationships:
        - Many-to-one with CustomUser via user field
        - One-to-many with Transaction via transactions reverse relation
        - Related name: user.accounts

    Balance Calculation:
        Balance is automatically recalculated when transactions are
        created, updated, or deleted through signals in transactions/signals.py

    Security:
        All queries MUST filter by user=request.user to ensure data isolation

    Example:
        account = Account.objects.create(
            user=request.user,
            name='Conta Corrente',
            bank_name='Banco do Brasil',
            account_type=Account.CHECKING,
            balance=1000.00
        )
    '''

    # Account type choices
    CHECKING = 'checking'
    SAVINGS = 'savings'
    WALLET = 'wallet'

    ACCOUNT_TYPE_CHOICES = [
        (CHECKING, 'Conta Corrente'),
        (SAVINGS, 'Conta Poupança'),
        (WALLET, 'Carteira'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='accounts',
        verbose_name='Usuário'
    )
    name = models.CharField(
        max_length=100,
        verbose_name='Nome da Conta'
    )
    bank_name = models.CharField(
        max_length=100,
        verbose_name='Nome do Banco'
    )
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        default=CHECKING,
        verbose_name='Tipo de Conta'
    )
    balance = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        verbose_name='Saldo'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo'
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
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'
        ordering = ['name']
        indexes = [
            models.Index(fields=['user', 'is_active']),
            models.Index(fields=['user', 'account_type']),
            models.Index(fields=['-created_at']),
        ]

    def __str__(self):
        '''
        Return string representation of the account.

        Returns:
            str: The account name
        '''
        return f'{self.name} - {self.bank_name}'
