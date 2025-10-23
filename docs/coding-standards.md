# Padrões de Código

Este documento define os guidelines e convenções de código do projeto Finanpy.

## Princípios Gerais

### 1. Simplicidade
- Evite over-engineering
- Prefira soluções diretas e claras
- YAGNI (You Aren't Gonna Need It)
- DRY (Don't Repeat Yourself)

### 2. Legibilidade
- Código deve ser autodocumentado
- Nomes descritivos são preferíveis a comentários
- Mantenha funções e métodos pequenos e focados

### 3. Consistência
- Siga os padrões estabelecidos no projeto
- Use as mesmas convenções em todo o código
- Mantenha a estrutura consistente entre apps

## Convenções de Código Python

### PEP 8
Todo código Python deve seguir a [PEP 8](https://peps.python.org/pep-0008/).

**Principais pontos**:
- Indentação: 4 espaços
- Linha máxima: 79 caracteres (flexível até 120 quando necessário)
- Linhas em branco: 2 entre classes, 1 entre métodos
- Imports sempre no topo do arquivo

### Aspas
**Use aspas simples** em todo o código Python:

```python
# Correto
name = 'John Doe'
message = 'Hello World'

# Incorreto
name = "John Doe"
message = "Hello World"
```

**Exceção**: Use aspas duplas quando a string contém aspas simples:
```python
message = "It's a beautiful day"
```

### Nomenclatura

#### Variáveis e Funções
- **snake_case** para variáveis e funções
- Nomes descritivos em inglês

```python
# Correto
user_name = 'John'
total_amount = 1000.50

def calculate_balance():
    pass

def get_user_transactions():
    pass

# Incorreto
userName = 'John'
TotalAmount = 1000.50

def CalculateBalance():
    pass
```

#### Classes
- **PascalCase** para classes

```python
# Correto
class UserProfile:
    pass

class BankAccount:
    pass

# Incorreto
class user_profile:
    pass

class bankAccount:
    pass
```

#### Constantes
- **UPPER_CASE** para constantes

```python
# Correto
MAX_AMOUNT = 10000
DEFAULT_CURRENCY = 'BRL'

# Incorreto
max_amount = 10000
default_currency = 'BRL'
```

### Imports
Organize imports em três grupos, separados por linha em branco:

```python
# 1. Standard library
from datetime import datetime
from decimal import Decimal

# 2. Django imports
from django.db import models
from django.contrib.auth.models import User

# 3. Local imports
from .models import Account
from categories.models import Category
```

Evite imports com `*`:
```python
# Incorreto
from django.db.models import *

# Correto
from django.db.models import Model, CharField, DecimalField
```

## Padrões Django

### Models

#### Estrutura do Model
```python
from django.db import models
from django.contrib.auth.models import User

class Account(models.Model):
    # Relacionamentos primeiro
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    # Campos principais
    name = models.CharField(max_length=100)
    bank_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=50)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    # Status
    is_active = models.BooleanField(default=True)

    # Timestamps (obrigatórios em todos os models)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'
        ordering = ['-created_at']

    def __str__(self):
        return self.name
```

#### Timestamps Obrigatórios
**Todos os models** devem ter os campos:
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

#### Meta Class
Sempre defina:
- `verbose_name` e `verbose_name_plural`
- `ordering` quando houver ordem padrão
- `unique_together` quando aplicável

#### __str__ Method
Todo model deve ter um método `__str__` descritivo:
```python
def __str__(self):
    return f'{self.name} - {self.bank_name}'
```

### Views

#### Function-Based Views (FBV)
```python
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

@login_required
def account_list(request):
    accounts = Account.objects.filter(user=request.user)
    context = {
        'accounts': accounts,
    }
    return render(request, 'accounts/list.html', context)
```

#### Class-Based Views (CBV)
```python
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

class AccountListView(LoginRequiredMixin, ListView):
    model = Account
    template_name = 'accounts/list.html'
    context_object_name = 'accounts'

    def get_queryset(self):
        return Account.objects.filter(user=self.request.user)
```

### Forms

```python
from django import forms
from .models import Account

class AccountForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ['name', 'bank_name', 'account_type', 'balance']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'balance': forms.NumberInput(attrs={'class': 'form-control'}),
        }
```

### URLs

```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('', views.account_list, name='list'),
    path('create/', views.account_create, name='create'),
    path('<int:pk>/edit/', views.account_edit, name='edit'),
    path('<int:pk>/delete/', views.account_delete, name='delete'),
]
```

**Convenções**:
- Use `app_name` para namespacing
- Use nomes descritivos para URLs
- Prefira trailing slash

## Templates

### Estrutura de Diretórios
```
accounts/
  templates/
    accounts/
      list.html
      form.html
      detail.html
```

### Nomenclatura
- `list.html`: Para listagens
- `form.html`: Para criar/editar
- `detail.html`: Para detalhes
- `confirm_delete.html`: Para confirmação de exclusão

### Convenções
```django
{% load static %}

<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <title>{% block title %}Finanpy{% endblock %}</title>
</head>
<body>
    {% block content %}
    {% endblock %}
</body>
</html>
```

## Segurança

### Proteção de Rotas
```python
# Use @login_required em views
@login_required
def my_view(request):
    pass

# Use LoginRequiredMixin em CBVs
class MyView(LoginRequiredMixin, View):
    pass
```

### Isolamento de Dados
Sempre filtre dados pelo usuário logado:
```python
# Correto
accounts = Account.objects.filter(user=request.user)

# Incorreto - expõe dados de outros usuários
accounts = Account.objects.all()
```

### Validação de Input
```python
# Sempre use forms para validação
form = AccountForm(request.POST)
if form.is_valid():
    account = form.save(commit=False)
    account.user = request.user
    account.save()
```

## Boas Práticas

### QuerySets Eficientes
```python
# Use select_related para ForeignKeys
accounts = Account.objects.select_related('user').all()

# Use prefetch_related para relações reversas
users = User.objects.prefetch_related('account_set').all()

# Evite N+1 queries
for account in accounts:
    print(account.user.email)  # Já foi carregado com select_related
```

### Uso de Managers
```python
class AccountManager(models.Manager):
    def active(self):
        return self.filter(is_active=True)

    def for_user(self, user):
        return self.filter(user=user)

class Account(models.Model):
    # ...
    objects = AccountManager()

# Uso
active_accounts = Account.objects.active()
user_accounts = Account.objects.for_user(request.user)
```

### Tratamento de Erros
```python
from django.shortcuts import get_object_or_404

# Use get_object_or_404
account = get_object_or_404(Account, pk=pk, user=request.user)

# Ou trate exceções explicitamente
try:
    account = Account.objects.get(pk=pk, user=request.user)
except Account.DoesNotExist:
    return redirect('accounts:list')
```

## Testes

### Nomenclatura
```python
# Nome do arquivo: test_models.py, test_views.py, test_forms.py

class AccountModelTest(TestCase):
    def test_create_account(self):
        pass

    def test_account_str_representation(self):
        pass
```

### Estrutura
```python
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Account

class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test',
            email='test@test.com',
            password='testpass123'
        )

    def test_create_account(self):
        account = Account.objects.create(
            user=self.user,
            name='Test Account',
            bank_name='Test Bank',
            balance=1000.00
        )
        self.assertEqual(account.name, 'Test Account')
        self.assertEqual(account.balance, 1000.00)
```

## Git

### Commits
- Mensagens em português
- Use o imperativo: "Adiciona", "Remove", "Corrige"
- Seja descritivo mas conciso

```
# Bom
Adiciona model Account com campos básicos
Corrige cálculo de saldo em Transaction
Remove campo desnecessário de Profile

# Ruim
fix bug
update
changes
```

### Branches
- `main`: Código em produção
- `develop`: Código em desenvolvimento
- `feature/nome-feature`: Novas funcionalidades
- `fix/nome-bug`: Correções de bugs

## Comentários

### Quando Comentar
- Lógica complexa que não pode ser simplificada
- Decisões de design não óbvias
- Workarounds temporários (com TODO)

### Como Comentar
```python
# Comentários de linha única começam com # e espaço

def complex_calculation():
    # TODO: Refatorar este cálculo quando tivermos mais dados
    # Este cálculo usa aproximação porque X razão
    result = (value * 1.5) + offset
    return result
```

### Docstrings
```python
def calculate_balance(account_id):
    """
    Calculate the current balance of an account.

    Args:
        account_id (int): The ID of the account

    Returns:
        Decimal: The current balance

    Raises:
        Account.DoesNotExist: If account not found
    """
    pass
```

## Checklist de Qualidade

Antes de commitar código, verifique:

- [ ] Código segue PEP 8
- [ ] Usa aspas simples
- [ ] Nomes em inglês
- [ ] Models têm created_at e updated_at
- [ ] Views protegidas com @login_required
- [ ] Dados filtrados por usuário
- [ ] Imports organizados
- [ ] Sem código comentado
- [ ] Sem prints de debug
- [ ] Testes passando (quando aplicável)
