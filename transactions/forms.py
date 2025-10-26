from datetime import date
from decimal import Decimal

from django import forms

from accounts.models import Account
from categories.models import Category

from .models import Transaction


class TransactionForm(forms.ModelForm):
    """
    Formulário para criação e edição de transações financeiras.
    """

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self._original_instance = None

        if self.instance.pk:
            try:
                self._original_instance = Transaction.objects.select_related(
                    'account'
                ).get(pk=self.instance.pk)
            except Transaction.DoesNotExist:
                self._original_instance = None

        if self.user:
            self.fields['account'].queryset = Account.objects.filter(
                user=self.user
            ).order_by('name')
            self.fields['category'].queryset = Category.objects.filter(
                user=self.user
            ).order_by('name')

        self.fields['account'].widget.attrs.update({
            'class': 'form-select w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
        })
        self.fields['category'].widget.attrs.update({
            'class': 'form-select w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
        })
        self.fields['transaction_type'].widget.attrs.update({
            'class': 'form-select w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
        })
        self.fields['amount'].widget.attrs.update({
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            'placeholder': '0,00',
            'step': '0.01',
        })
        self.fields['transaction_date'].widget = forms.DateInput(attrs={
            'type': 'date',
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
        })
        self.fields['description'].widget = forms.Textarea(attrs={
            'rows': 3,
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            'placeholder': 'Descreva esta transação',
        })

    class Meta:
        model = Transaction
        fields = [
            'account',
            'category',
            'transaction_type',
            'amount',
            'transaction_date',
            'description',
        ]
        labels = {
            'account': 'Conta',
            'category': 'Categoria',
            'transaction_type': 'Tipo de Transação',
            'amount': 'Valor',
            'transaction_date': 'Data',
            'description': 'Descrição',
        }

    def clean_amount(self):
        amount = self.cleaned_data.get('amount')
        if amount is not None and amount <= 0:
            raise forms.ValidationError('O valor da transação deve ser positivo.')
        return amount

    def clean_transaction_date(self):
        transaction_date = self.cleaned_data.get('transaction_date')
        if transaction_date and transaction_date > date.today():
            raise forms.ValidationError('A data da transação não pode ser no futuro.')
        return transaction_date

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        transaction_type = cleaned_data.get('transaction_type')
        account = cleaned_data.get('account')
        amount = cleaned_data.get('amount')

        if account and self.user and account.user_id != self.user.id:
            self.add_error('account', 'Selecione uma conta válida.')

        if category and self.user and category.user_id != self.user.id:
            self.add_error('category', 'Selecione uma categoria válida.')

        if category and transaction_type and category.category_type != transaction_type:
            self.add_error(
                'category',
                'A categoria selecionada deve corresponder ao tipo de transação.',
            )

        self.balance_warning = None
        if (
            transaction_type == Transaction.TransactionType.EXPENSE
            and account
            and amount
        ):
            available_balance = self._get_available_balance(account)
            if available_balance < amount:
                self.add_error(
                    'amount',
                    'Saldo insuficiente na conta selecionada para esta transação.',
                )

        return cleaned_data

    def _get_available_balance(self, account):
        """
        Return the available balance for the given account considering updates.
        """
        available_balance = account.balance

        if (
            self._original_instance
            and self._original_instance.account_id == account.id
        ):
            previous_delta = self._calculate_delta(
                self._original_instance.amount,
                self._original_instance.transaction_type,
            )
            available_balance = account.balance - previous_delta

        return available_balance

    @staticmethod
    def _calculate_delta(amount, transaction_type):
        """
        Calculate how the transaction amount affects the account balance.
        """
        if transaction_type == Transaction.TransactionType.INCOME:
            return amount
        return amount * Decimal('-1')
