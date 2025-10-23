from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

User = get_user_model()


class LoginForm(forms.Form):
    """
    Custom login form for user authentication.

    Uses email (not username) as the identifier field, matching CustomUser configuration.
    Includes TailwindCSS styling for consistent UI design.
    """

    email = forms.EmailField(
        label='Email',
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            'placeholder': 'seu@email.com',
        })
    )

    password = forms.CharField(
        label='Senha',
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            'placeholder': 'Digite sua senha',
        })
    )


class SignupForm(UserCreationForm):
    """
    Custom signup form for user registration.

    Uses email as the primary identifier (no username field).
    Includes custom validation for unique email and TailwindCSS styling.
    """

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            'placeholder': 'seu@email.com',
        })
    )

    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            'placeholder': 'Digite sua senha',
        })
    )

    password2 = forms.CharField(
        label='Confirme a senha',
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition duration-200',
            'placeholder': 'Digite sua senha novamente',
        })
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def clean_email(self):
        """
        Validate that the email is unique in the database.

        Returns:
            str: The cleaned email address

        Raises:
            ValidationError: If email already exists in database
        """
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            raise ValidationError(
                'Este email já está cadastrado. Por favor, use outro email ou faça login.',
                code='duplicate_email'
            )

        return email
