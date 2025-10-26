'''
Signal handlers for automatic account balance updates.

This module contains signals that automatically update account balances
when transactions are created, updated, or deleted. All balance updates
use F() expressions to avoid race conditions.

Key Behavior:
    - CREATE: Adds/subtracts from balance based on transaction type
    - UPDATE: Reverses old effect, applies new effect (atomic)
    - DELETE: Reverses the transaction effect

Balance Calculation:
    - INCOME transactions: Add to balance (+)
    - EXPENSE transactions: Subtract from balance (-)
'''
from decimal import Decimal

from django.db import transaction as db_transaction
from django.db.models import F
from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver

from accounts.models import Account

from .models import Transaction


def _calculate_delta(amount: Decimal, transaction_type: str) -> Decimal:
    '''
    Calculate the balance delta based on transaction type.

    INCOME transactions return positive delta (adds to balance).
    EXPENSE transactions return negative delta (subtracts from balance).

    Args:
        amount: Transaction amount (always positive)
        transaction_type: Transaction.TransactionType.INCOME or EXPENSE

    Returns:
        Decimal: Positive for INCOME, negative for EXPENSE

    Example:
        >>> _calculate_delta(Decimal('100.00'), 'INCOME')
        Decimal('100.00')
        >>> _calculate_delta(Decimal('100.00'), 'EXPENSE')
        Decimal('-100.00')
    '''
    if transaction_type == Transaction.TransactionType.INCOME:
        return amount
    return amount * Decimal('-1')


def _apply_delta(account_id: int, delta: Decimal) -> None:
    '''
    Apply balance delta to account using F() expression.

    Uses F() expressions to perform database-level arithmetic, avoiding
    race conditions when multiple transactions update the same account.
    This ensures thread-safe balance updates.

    Args:
        account_id: Primary key of the Account to update
        delta: Amount to add/subtract (can be positive or negative)

    Note:
        F() expressions prevent race conditions by performing the
        calculation at the database level, not in Python memory.
    '''
    Account.objects.filter(pk=account_id).update(balance=F('balance') + delta)


@receiver(post_save, sender=Transaction)
def update_balance_on_create(sender, instance, created, **kwargs):
    '''
    Signal handler: Update account balance when new transaction is created.

    This signal fires after a Transaction is saved. If it's a new transaction
    (created=True), it automatically updates the associated account's balance.

    Balance changes:
        - INCOME: Adds amount to account balance
        - EXPENSE: Subtracts amount from account balance

    Args:
        sender: The Transaction model class
        instance: The Transaction instance being saved
        created: Boolean indicating if this is a new transaction
        **kwargs: Additional signal arguments

    Example:
        # Creating a new INCOME transaction of R$ 1000
        # Account balance: R$ 500 -> R$ 1500 (automatic)
    '''
    if not created:
        return

    # Calculate and apply balance change
    delta = _calculate_delta(instance.amount, instance.transaction_type)
    _apply_delta(instance.account_id, delta)


@receiver(pre_save, sender=Transaction)
def update_balance_on_update(sender, instance, **kwargs):
    '''
    Signal handler: Recalculate balances when transaction is updated.

    This signal fires BEFORE a Transaction is updated. It reverts the old
    balance effect and applies the new one atomically. Handles changes to:
    - Transaction amount
    - Transaction type (INCOME <-> EXPENSE)
    - Associated account

    The operation is atomic to prevent inconsistent balance states.

    Args:
        sender: The Transaction model class
        instance: The Transaction instance being updated
        **kwargs: Additional signal arguments

    Note:
        Uses pre_save (not post_save) to access the previous values
        before they're overwritten in the database.

    Example:
        # Updating transaction from R$ 100 EXPENSE to R$ 200 EXPENSE
        # Step 1: Revert old effect (+100 to balance)
        # Step 2: Apply new effect (-200 to balance)
        # Net effect: Balance decreases by R$ 100
    '''
    # Skip if this is a new transaction (no pk yet)
    if not instance.pk:
        return

    # Fetch the previous transaction state from database
    try:
        previous = Transaction.objects.select_related('account').get(pk=instance.pk)
    except Transaction.DoesNotExist:
        return

    # Calculate old and new balance effects
    previous_delta = _calculate_delta(previous.amount, previous.transaction_type)
    new_delta = _calculate_delta(instance.amount, instance.transaction_type)

    # Skip if nothing changed that affects balance
    # (e.g., only description was updated)
    if (
        previous.account_id == instance.account_id
        and previous_delta == new_delta
    ):
        return

    # Atomically update balances to avoid race conditions
    with db_transaction.atomic():
        # Step 1: Revert the previous balance effect
        _apply_delta(previous.account_id, -previous_delta)

        # Step 2: Apply the new balance effect
        _apply_delta(instance.account_id, new_delta)


@receiver(post_delete, sender=Transaction)
def update_balance_on_delete(sender, instance, **kwargs):
    '''
    Signal handler: Revert balance when transaction is deleted.

    This signal fires after a Transaction is deleted. It automatically
    reverses the transaction's effect on the account balance.

    Balance changes (reversed):
        - INCOME: Subtracts amount from account balance
        - EXPENSE: Adds amount back to account balance

    Args:
        sender: The Transaction model class
        instance: The Transaction instance being deleted
        **kwargs: Additional signal arguments

    Example:
        # Deleting an EXPENSE transaction of R$ 100
        # Account balance: R$ 400 -> R$ 500 (automatic revert)
    '''
    # Calculate the original delta and reverse it
    delta = _calculate_delta(instance.amount, instance.transaction_type)
    _apply_delta(instance.account_id, -delta)
