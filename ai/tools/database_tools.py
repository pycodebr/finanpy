'''
LangChain database tools for accessing Finanpy financial data.

This module provides tools that allow AI agents to query Django ORM
for user-specific financial information including transactions, accounts,
categories, and spending analysis.

All tools require user_id parameter and enforce strict data isolation.
'''

from datetime import datetime, timedelta
from decimal import Decimal
from typing import Dict, List

from django.db.models import Count, Sum

from langchain.tools import tool

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction


@tool
def get_user_transactions(user_id: int) -> List[Dict]:
    '''
    Retrieve user transactions from the last 30 days.

    This tool fetches all financial transactions for a specific user
    from the past 30 days, including details about date, amount, type,
    category, and description. Results are ordered by most recent first.

    Args:
        user_id (int): The ID of the user whose transactions to retrieve.
                      Must be a valid user ID in the system.

    Returns:
        List[Dict]: List of transaction dictionaries with the following keys:
            - date (str): Transaction date in YYYY-MM-DD format
            - amount (float): Transaction amount in BRL
            - type (str): Transaction type ('INCOME' or 'EXPENSE')
            - category (str): Category name
            - description (str): Transaction description (may be empty)
            - account (str): Account name where transaction occurred

    Example:
        >>> get_user_transactions(5)
        [
            {
                'date': '2025-11-03',
                'amount': 150.00,
                'type': 'EXPENSE',
                'category': 'Alimentação',
                'description': 'Supermercado',
                'account': 'Conta Corrente'
            },
            ...
        ]

    Note:
        - Only returns transactions from the last 30 days
        - Automatically filters by user_id for data isolation
        - Uses select_related for optimized database queries
        - Returns empty list if user has no transactions
    '''
    try:
        # Calculate date 30 days ago from today
        thirty_days_ago = datetime.now().date() - timedelta(days=30)

        # Query transactions with related account and category
        transactions = Transaction.objects.filter(
            account__user_id=user_id,
            transaction_date__gte=thirty_days_ago
        ).select_related(
            'account',
            'category'
        ).order_by('-transaction_date')

        # Serialize to JSON-compatible format
        result = []
        for txn in transactions:
            result.append({
                'date': txn.transaction_date.strftime('%Y-%m-%d'),
                'amount': float(txn.amount),
                'type': txn.transaction_type,
                'category': txn.category.name,
                'description': txn.description,
                'account': txn.account.name
            })

        return result

    except Exception:
        # Return empty list on error to prevent agent failure
        return []


@tool
def get_user_accounts(user_id: int) -> List[Dict]:
    '''
    Retrieve all user accounts with current balances.

    This tool fetches all bank accounts, savings accounts, and wallets
    belonging to a specific user, including their names, bank information,
    and current balance.

    Args:
        user_id (int): The ID of the user whose accounts to retrieve.
                      Must be a valid user ID in the system.

    Returns:
        List[Dict]: List of account dictionaries with the following keys:
            - name (str): Account name (e.g., 'Conta Principal')
            - bank_name (str): Name of the financial institution
            - account_type (str): Type of account ('checking', 'savings', 'wallet')
            - balance (float): Current account balance in BRL
            - is_active (bool): Whether the account is currently active

    Example:
        >>> get_user_accounts(5)
        [
            {
                'name': 'Conta Corrente',
                'bank_name': 'Banco do Brasil',
                'account_type': 'checking',
                'balance': 2500.00,
                'is_active': True
            },
            ...
        ]

    Note:
        - Automatically filters by user_id for data isolation
        - Returns empty list if user has no accounts
        - Balance is calculated from transaction signals
    '''
    try:
        # Query accounts for the user
        accounts = Account.objects.filter(user_id=user_id)

        # Serialize to JSON-compatible format
        result = []
        for account in accounts:
            result.append({
                'name': account.name,
                'bank_name': account.bank_name,
                'account_type': account.account_type,
                'balance': float(account.balance),
                'is_active': account.is_active
            })

        return result

    except Exception:
        # Return empty list on error to prevent agent failure
        return []


@tool
def get_user_categories(user_id: int) -> List[Dict]:
    '''
    Retrieve all user categories with their types.

    This tool fetches all transaction categories (both income and expense)
    that belong to a specific user, including their names and types.

    Args:
        user_id (int): The ID of the user whose categories to retrieve.
                      Must be a valid user ID in the system.

    Returns:
        List[Dict]: List of category dictionaries with the following keys:
            - name (str): Category name (e.g., 'Alimentação', 'Salário')
            - type (str): Category type ('INCOME' or 'EXPENSE')
            - color (str): Hex color code for UI display

    Example:
        >>> get_user_categories(5)
        [
            {
                'name': 'Salário',
                'type': 'INCOME',
                'color': '#10b981'
            },
            {
                'name': 'Alimentação',
                'type': 'EXPENSE',
                'color': '#ef4444'
            },
            ...
        ]

    Note:
        - Automatically filters by user_id for data isolation
        - Returns empty list if user has no categories
        - Categories are ordered alphabetically by name
    '''
    try:
        # Query categories for the user
        categories = Category.objects.filter(user_id=user_id).order_by('name')

        # Serialize to JSON-compatible format
        result = []
        for category in categories:
            result.append({
                'name': category.name,
                'type': category.category_type,
                'color': category.color
            })

        return result

    except Exception:
        # Return empty list on error to prevent agent failure
        return []


@tool
def get_spending_by_category(user_id: int) -> List[Dict]:
    '''
    Get total spending per category for the last 30 days.

    This tool calculates the total amount spent in each expense category
    over the past 30 days, ordered from highest to lowest spending.
    Only EXPENSE transactions are included in this analysis.

    Args:
        user_id (int): The ID of the user whose spending to analyze.
                      Must be a valid user ID in the system.

    Returns:
        List[Dict]: List of category spending dictionaries with the following keys:
            - category (str): Category name
            - total (float): Total amount spent in BRL
            - transaction_count (int): Number of transactions in this category
            - percentage (float): Percentage of total spending (0-100)

    Example:
        >>> get_spending_by_category(5)
        [
            {
                'category': 'Alimentação',
                'total': 1200.00,
                'transaction_count': 15,
                'percentage': 35.5
            },
            {
                'category': 'Transporte',
                'total': 800.00,
                'transaction_count': 20,
                'percentage': 23.7
            },
            ...
        ]

    Note:
        - Only includes EXPENSE transactions (not INCOME)
        - Only analyzes the last 30 days
        - Results are ordered by total amount (highest first)
        - Returns empty list if user has no expenses
        - Percentage is relative to total expenses in the period
    '''
    try:
        # Calculate date 30 days ago from today
        thirty_days_ago = datetime.now().date() - timedelta(days=30)

        # Query expenses by category with aggregation
        category_spending = Transaction.objects.filter(
            account__user_id=user_id,
            transaction_date__gte=thirty_days_ago,
            transaction_type=Transaction.TransactionType.EXPENSE
        ).values(
            'category__name'
        ).annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-total')

        # Calculate total spending for percentage calculation
        total_spending = sum(item['total'] for item in category_spending)

        # Serialize to JSON-compatible format with percentages
        result = []
        for item in category_spending:
            total_amount = float(item['total'] or Decimal('0.00'))
            percentage = (total_amount / float(total_spending) * 100) if total_spending > 0 else 0

            result.append({
                'category': item['category__name'],
                'total': total_amount,
                'transaction_count': item['count'],
                'percentage': round(percentage, 1)
            })

        return result

    except Exception:
        # Return empty list on error to prevent agent failure
        return []


@tool
def get_income_vs_expense(user_id: int) -> Dict:
    '''
    Calculate total income vs expenses for the last 30 days.

    This tool provides a financial summary showing total income,
    total expenses, and net balance (income - expenses) for a user
    over the past 30 days.

    Args:
        user_id (int): The ID of the user whose financial summary to calculate.
                      Must be a valid user ID in the system.

    Returns:
        Dict: Financial summary dictionary with the following keys:
            - total_income (float): Total income in BRL
            - total_expense (float): Total expenses in BRL
            - balance (float): Net balance (income - expenses) in BRL
            - income_count (int): Number of income transactions
            - expense_count (int): Number of expense transactions
            - period_days (int): Number of days analyzed (30)

    Example:
        >>> get_income_vs_expense(5)
        {
            'total_income': 5000.00,
            'total_expense': 3500.00,
            'balance': 1500.00,
            'income_count': 3,
            'expense_count': 45,
            'period_days': 30
        }

    Note:
        - Analyzes exactly the last 30 days
        - Automatically filters by user_id for data isolation
        - Positive balance indicates surplus, negative indicates deficit
        - Returns zeros if user has no transactions
    '''
    try:
        # Calculate date 30 days ago from today
        thirty_days_ago = datetime.now().date() - timedelta(days=30)

        # Calculate total income
        income_data = Transaction.objects.filter(
            account__user_id=user_id,
            transaction_date__gte=thirty_days_ago,
            transaction_type=Transaction.TransactionType.INCOME
        ).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )

        # Calculate total expenses
        expense_data = Transaction.objects.filter(
            account__user_id=user_id,
            transaction_date__gte=thirty_days_ago,
            transaction_type=Transaction.TransactionType.EXPENSE
        ).aggregate(
            total=Sum('amount'),
            count=Count('id')
        )

        # Extract values with default to 0
        total_income = float(income_data['total'] or Decimal('0.00'))
        total_expense = float(expense_data['total'] or Decimal('0.00'))
        income_count = income_data['count'] or 0
        expense_count = expense_data['count'] or 0

        # Calculate balance
        balance = total_income - total_expense

        return {
            'total_income': total_income,
            'total_expense': total_expense,
            'balance': balance,
            'income_count': income_count,
            'expense_count': expense_count,
            'period_days': 30
        }

    except Exception:
        # Return zeros on error to prevent agent failure
        return {
            'total_income': 0.0,
            'total_expense': 0.0,
            'balance': 0.0,
            'income_count': 0,
            'expense_count': 0,
            'period_days': 30
        }
