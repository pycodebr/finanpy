from django import forms

from .models import Account


class AccountForm(forms.ModelForm):
    """
    Form for creating and editing bank accounts.

    Includes all editable fields with TailwindCSS styling and Portuguese labels.
    Account type choices are displayed in Portuguese matching the model configuration.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['balance'].widget.attrs['readonly'] = True
            self.fields['balance'].widget.attrs['class'] += ' bg-slate-800 text-slate-400 cursor-not-allowed'
            self.fields['balance'].label = 'Saldo Atual'
            self.initial['balance'] = f'{self.instance.balance:.2f}'.replace(',', '.')
        if not self.instance.pk:
            self.fields['is_active'].initial = True

    class Meta:
        model = Account
        fields = ['name', 'bank_name', 'account_type', 'balance', 'is_active']

        labels = {
            'name': 'Nome da Conta',
            'bank_name': 'Nome do Banco',
            'account_type': 'Tipo de Conta',
            'balance': 'Saldo Inicial',
            'is_active': 'Ativa',
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
                'class': 'form-select w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            }),
            'balance': forms.NumberInput(attrs={
                'class': 'w-full pl-12 pr-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': '0.00',
                'step': '0.01',
                'min': '0',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'h-5 w-5 rounded border-slate-500 bg-slate-700 text-purple-600 focus:ring-purple-500 focus:ring-offset-slate-800',
            }),
        }

    def clean_balance(self):
        balance = self.cleaned_data.get('balance')
        if balance is not None and balance < 0:
            raise forms.ValidationError('O saldo inicial não pode ser negativo.')
        return balance
