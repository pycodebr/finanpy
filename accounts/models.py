from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Account(models.Model):
    """
    Model representing a bank account or wallet.

    Each account belongs to a specific user and can be of different types:
    checking, savings, or wallet. Accounts track their balance and can be
    activated/deactivated.
    """

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
        """Return the account name."""
        return self.name
