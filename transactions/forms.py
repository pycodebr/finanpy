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
            raise forms.ValidationError('O valor deve ser positivo.')
        return amount

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get('category')
        transaction_type = cleaned_data.get('transaction_type')
        account = cleaned_data.get('account')

        if account and self.user and account.user_id != self.user.id:
            self.add_error('account', 'Selecione uma conta válida.')

        if category and self.user and category.user_id != self.user.id:
            self.add_error('category', 'Selecione uma categoria válida.')

        if category and transaction_type and category.category_type != transaction_type:
            self.add_error(
                'category',
                'A categoria selecionada deve corresponder ao tipo de transação.',
            )

        return cleaned_data
