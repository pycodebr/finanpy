from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    """
    Form for creating and editing bank accounts.

    Includes all editable fields with TailwindCSS styling and Portuguese labels.
    Account type choices are displayed in Portuguese matching the model configuration.
    """

    class Meta:
        model = Account
        fields = ['name', 'bank_name', 'account_type', 'balance']

        labels = {
            'name': 'Nome da Conta',
            'bank_name': 'Nome do Banco',
            'account_type': 'Tipo de Conta',
            'balance': 'Saldo Inicial',
        }

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': 'Ex: Conta Pessoal, Investimentos',
            }),
            'bank_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': 'Ex: Banco do Brasil, Nubank',
            }),
            'account_type': forms.Select(attrs={
                'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
        }
