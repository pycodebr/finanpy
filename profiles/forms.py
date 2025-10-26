from django import forms
from django.core.validators import RegexValidator

from .models import Profile


class ProfileForm(forms.ModelForm):
    """
    Form for updating user profile information.

    Includes validation for phone number format and TailwindCSS styling.
    All fields are optional to allow partial profile updates.
    """

    # Optional phone validator - allows common phone formats
    phone_validator = RegexValidator(
        regex=r'^[\d\s\-\(\)\+]+$',
        message='Formato de telefone inválido. Use apenas números, espaços, parênteses, hífens ou sinal de +.'
    )

    class Meta:
        model = Profile
        fields = ['full_name', 'phone']

        labels = {
            'full_name': 'Nome Completo',
            'phone': 'Telefone',
        }

        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': 'Ex: João Silva',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
                'placeholder': 'Ex: (11) 98765-4321',
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Initialize the form and add phone validation if field has content.
        """
        super().__init__(*args, **kwargs)
        # Add validator to phone field
        self.fields['phone'].validators.append(self.phone_validator)

    def clean_phone(self):
        """
        Clean and validate phone number.

        Returns:
            str: Cleaned phone number

        Raises:
            ValidationError: If phone format is invalid
        """
        phone = self.cleaned_data.get('phone', '').strip()
        # If phone is empty, it's valid (field is optional)
        if not phone:
            return phone
        # Additional validation can be added here if needed
        return phone
