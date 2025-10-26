from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import F
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from accounts.models import Account

from .models import Transaction


def _calculate_delta(amount: Decimal, transaction_type: str) -> Decimal:
    """
    Return the balance delta based on transaction type.
    """
    if transaction_type == Transaction.TransactionType.INCOME:
        return amount
    return amount * Decimal('-1')


def _apply_delta(account_id: int, delta: Decimal) -> None:
    """
    Apply the delta to the account balance using F expressions.
    """
    Account.objects.filter(pk=account_id).update(balance=F('balance') + delta)


@receiver(post_save, sender=Transaction)
def update_balance_on_create(sender, instance, created, **kwargs):
    """
    Update account balance when a new transaction is created.
    """
    if not created:
        return

    delta = _calculate_delta(instance.amount, instance.transaction_type)
    _apply_delta(instance.account_id, delta)


@receiver(pre_save, sender=Transaction)
def update_balance_on_update(sender, instance, **kwargs):
    """
    Recalculate account balances when a transaction is updated.
    """
    if not instance.pk:
        return

    try:
        previous = Transaction.objects.select_related('account').get(pk=instance.pk)
    except Transaction.DoesNotExist:
        return

    previous_delta = _calculate_delta(previous.amount, previous.transaction_type)
    new_delta = _calculate_delta(instance.amount, instance.transaction_type)

    # Skip if nothing changed affecting balance
    if (
        previous.account_id == instance.account_id
        and previous_delta == new_delta
    ):
        return

    with db_transaction.atomic():
        # Revert previous effect
        _apply_delta(previous.account_id, -previous_delta)

        # Apply new effect
        _apply_delta(instance.account_id, new_delta)


@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    """
    Revert account balance when a transaction is deleted.
    """
    delta = _calculate_delta(instance.amount, instance.transaction_type)
    _apply_delta(instance.account_id, -delta)
