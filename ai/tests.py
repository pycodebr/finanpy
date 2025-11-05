from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase

from accounts.models import Account
from categories.models import Category
from transactions.models import Transaction

from ai.tools.database_tools import (
    get_income_vs_expense,
    get_spending_by_category,
    get_user_accounts,
    get_user_categories,
    get_user_transactions
)


class DatabaseToolsIsolationTests(TestCase):
    def setUp(self):
        User = get_user_model()
        self.user_one = User.objects.create_user(email='user1@example.com', password='test123')
        self.user_two = User.objects.create_user(email='user2@example.com', password='test123')

        self.account_one = Account.objects.create(
            user=self.user_one,
            name='Conta Principal',
            bank_name='Banco do Brasil',
            account_type=Account.CHECKING,
            balance=1000
        )
        self.account_two = Account.objects.create(
            user=self.user_two,
            name='Conta Secundaria',
            bank_name='Nubank',
            account_type=Account.CHECKING,
            balance=2000
        )

        self.category_food = Category.objects.create(
            user=self.user_one,
            name='Alimentacao',
            category_type=Category.CategoryType.EXPENSE,
            color='#f97316'
        )
        self.category_salary = Category.objects.create(
            user=self.user_one,
            name='Salario',
            category_type=Category.CategoryType.INCOME,
            color='#22c55e'
        )

        Transaction.objects.create(
            account=self.account_one,
            category=self.category_salary,
            description='Salario Mensal',
            amount=5000,
            transaction_type=Transaction.TransactionType.INCOME,
            transaction_date=date.today()
        )
        Transaction.objects.create(
            account=self.account_one,
            category=self.category_food,
            description='Mercado',
            amount=350,
            transaction_type=Transaction.TransactionType.EXPENSE,
            transaction_date=date.today() - timedelta(days=3)
        )

    def test_transactions_are_isolated_by_user(self):
        data = get_user_transactions.invoke({'user_id': self.user_one.id})
        self.assertEqual(len(data), 2)
        self.assertTrue(all(item['account'] == self.account_one.name for item in data))

        data_other = get_user_transactions.invoke({'user_id': self.user_two.id})
        self.assertEqual(data_other, [])

    def test_accounts_and_categories_filtered(self):
        accounts = get_user_accounts.invoke({'user_id': self.user_one.id})
        self.assertEqual(len(accounts), 1)
        self.assertEqual(accounts[0]['name'], 'Conta Principal')

        categories = get_user_categories.invoke({'user_id': self.user_one.id})
        names = {cat['name'] for cat in categories}
        self.assertIn('Alimentacao', names)
        self.assertIn('Salario', names)
        self.assertTrue(
            all(Category.objects.filter(user=self.user_one, name=name).exists() for name in names)
        )

    def test_spending_and_income_vs_expense_summary(self):
        spending = get_spending_by_category.invoke({'user_id': self.user_one.id})
        self.assertTrue(any(item['category'] == 'Alimentacao' for item in spending))

        summary = get_income_vs_expense.invoke({'user_id': self.user_one.id})
        self.assertGreater(summary['total_income'], 0)
        self.assertGreater(summary['total_expense'], 0)

    def test_invalid_user_id_raises_value_error(self):
        with self.assertRaises(ValueError):
            get_user_transactions.invoke({'user_id': 0})

        with self.assertRaises(ValueError):
            get_user_transactions.invoke({'user_id': 'abc'})

        with self.assertRaises(ValueError):
            get_user_transactions.invoke({'user_id': 9999})
