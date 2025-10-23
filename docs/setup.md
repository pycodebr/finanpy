# Setup e Desenvolvimento

Este documento fornece instruções para configurar o ambiente de desenvolvimento e iniciar o projeto Finanpy.

## Pré-requisitos

- Python 3.13 ou superior
- pip (gerenciador de pacotes Python)
- Git
- Editor de código (recomendado: VS Code, PyCharm)

## Instalação

### 1. Clonar o Repositório

```bash
git clone <repository-url>
cd finanpy
```

### 2. Criar Ambiente Virtual

É altamente recomendado usar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar ambiente virtual
python -m venv .venv

# Ativar ambiente virtual (Linux/Mac)
source .venv/bin/activate

# Ativar ambiente virtual (Windows)
.venv\Scripts\activate
```

### 3. Instalar Dependências

```bash
pip install -r requirements.txt
```

**Dependências principais**:
- Django 5.2.7
- asgiref 3.10.0
- sqlparse 0.5.3

### 4. Configurar Banco de Dados

O projeto usa SQLite3 por padrão. Para criar o banco de dados e aplicar as migrations:

```bash
# Criar migrations (se necessário)
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate
```

Isso criará o arquivo `db.sqlite3` na raiz do projeto.

### 5. Criar Superusuário (Opcional)

Para acessar o Django Admin:

```bash
python manage.py createsuperuser
```

Siga as instruções para definir email e senha.

### 6. Executar o Servidor

```bash
python manage.py runserver
```

O servidor estará disponível em: `http://127.0.0.1:8000/`

---

## Estrutura do Projeto

```
finanpy/
├── .venv/              # Ambiente virtual (não commitado)
├── core/               # Configurações do Django
│   ├── settings.py     # Configurações principais
│   ├── urls.py         # URLs principais
│   ├── wsgi.py         # WSGI config
│   └── asgi.py         # ASGI config
├── users/              # App de usuários
├── profiles/           # App de perfis
├── accounts/           # App de contas bancárias
├── categories/         # App de categorias
├── transactions/       # App de transações
├── docs/               # Documentação
├── manage.py           # Script de gerenciamento Django
├── requirements.txt    # Dependências Python
├── db.sqlite3          # Banco de dados SQLite
└── PRD.md             # Product Requirements Document
```

---

## Comandos Úteis

### Gerenciamento Django

```bash
# Criar um novo app
python manage.py startapp <app_name>

# Criar migrations
python manage.py makemigrations

# Aplicar migrations
python manage.py migrate

# Verificar status das migrations
python manage.py showmigrations

# Abrir shell Django
python manage.py shell

# Coletar arquivos estáticos
python manage.py collectstatic
```

### Banco de Dados

```bash
# Resetar banco de dados (CUIDADO: apaga todos os dados)
rm db.sqlite3
python manage.py migrate

# Fazer backup do banco
cp db.sqlite3 db.sqlite3.backup

# Restaurar backup
cp db.sqlite3.backup db.sqlite3
```

### Django Admin

Acesse `http://127.0.0.1:8000/admin/` com as credenciais do superusuário.

---

## Workflow de Desenvolvimento

### 1. Antes de Começar

```bash
# Ativar ambiente virtual
source .venv/bin/activate

# Atualizar dependências (se houver)
pip install -r requirements.txt

# Aplicar migrations pendentes
python manage.py migrate
```

### 2. Durante o Desenvolvimento

```bash
# Executar servidor em modo de desenvolvimento
python manage.py runserver

# Em outro terminal, aplicar migrations quando criar/modificar models
python manage.py makemigrations
python manage.py migrate
```

### 3. Ao Criar Novos Models

```bash
# 1. Criar/modificar model em models.py
# 2. Criar migration
python manage.py makemigrations <app_name>

# 3. Revisar migration gerada em <app>/migrations/
# 4. Aplicar migration
python manage.py migrate

# 5. Registrar no admin (se necessário) em admin.py
```

### 4. Ao Finalizar

```bash
# Desativar ambiente virtual
deactivate
```

---

## Configuração do TailwindCSS

O projeto usa TailwindCSS para estilização. Para configurar:

### 1. Instalar Node.js e npm
Baixe e instale de: https://nodejs.org/

### 2. Inicializar TailwindCSS

```bash
# Instalar Tailwind via npm
npm install -D tailwindcss

# Criar configuração
npx tailwindcss init
```

### 3. Configurar tailwind.config.js

```javascript
module.exports = {
  content: [
    './templates/**/*.html',
    './*/templates/**/*.html',
  ],
  theme: {
    extend: {
      colors: {
        'primary-500': '#667eea',
        'accent-500': '#764ba2',
        'bg-primary': '#0f172a',
        'bg-secondary': '#1e293b',
        'bg-tertiary': '#334155',
      },
    },
  },
  plugins: [],
}
```

### 4. Criar arquivo CSS de entrada

```css
/* static/css/input.css */
@tailwind base;
@tailwind components;
@tailwind utilities;
```

### 5. Compilar CSS

```bash
npx tailwindcss -i ./static/css/input.css -o ./static/css/output.css --watch
```

---

## Variáveis de Ambiente

Para produção, utilize variáveis de ambiente para dados sensíveis.

### Criar arquivo .env (não commitado)

```bash
# .env
DEBUG=True
SECRET_KEY=sua-chave-secreta-aqui
DATABASE_URL=sqlite:///db.sqlite3
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Usar python-decouple

```bash
pip install python-decouple
```

```python
# settings.py
from decouple import config

SECRET_KEY = config('SECRET_KEY')
DEBUG = config('DEBUG', default=False, cast=bool)
```

---

## Testes

### Executar Testes

```bash
# Executar todos os testes
python manage.py test

# Executar testes de um app específico
python manage.py test <app_name>

# Executar testes com verbosidade
python manage.py test --verbosity=2

# Executar testes e manter banco de dados
python manage.py test --keepdb
```

### Estrutura de Testes

```
accounts/
  tests/
    __init__.py
    test_models.py
    test_views.py
    test_forms.py
```

### Exemplo de Teste

```python
# accounts/tests/test_models.py
from django.test import TestCase
from django.contrib.auth.models import User
from accounts.models import Account

class AccountModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='test@test.com',
            email='test@test.com',
            password='testpass123'
        )

    def test_create_account(self):
        account = Account.objects.create(
            user=self.user,
            name='Conta Teste',
            bank_name='Banco Teste',
            account_type='checking',
            balance=1000.00
        )
        self.assertEqual(account.name, 'Conta Teste')
        self.assertEqual(account.balance, 1000.00)
```

---

## Debugging

### Django Debug Toolbar (Recomendado)

```bash
# Instalar
pip install django-debug-toolbar

# Adicionar em settings.py
INSTALLED_APPS = [
    ...
    'debug_toolbar',
]

MIDDLEWARE = [
    ...
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

# Adicionar em urls.py
from django.urls import include

urlpatterns = [
    ...
    path('__debug__/', include('debug_toolbar.urls')),
]
```

### Print Debugging

```python
# Em views
print(f'User: {request.user}')
print(f'Accounts: {accounts.count()}')

# Em models
def save(self, *args, **kwargs):
    print(f'Saving {self.name}')
    super().save(*args, **kwargs)
```

### Django Shell

```bash
python manage.py shell

# Dentro do shell
from accounts.models import Account
accounts = Account.objects.all()
print(accounts)
```

---

## Boas Práticas

### Git Workflow

```bash
# Criar branch para nova feature
git checkout -b feature/nome-feature

# Fazer alterações e commits
git add .
git commit -m "Adiciona funcionalidade X"

# Atualizar branch com main
git checkout main
git pull origin main
git checkout feature/nome-feature
git merge main

# Push da branch
git push origin feature/nome-feature

# Criar Pull Request no GitHub
```

### Commits

- Use mensagens descritivas em português
- Use o imperativo: "Adiciona", "Corrige", "Remove"
- Seja específico mas conciso

**Exemplos**:
```
✓ Adiciona model Account com validações
✓ Corrige cálculo de saldo em Transaction
✓ Remove campo desnecessário de Profile
✗ fix
✗ update
✗ alterações
```

### Code Review

Antes de fazer commit, verifique:

- [ ] Código segue PEP 8
- [ ] Usa aspas simples
- [ ] Nomes em inglês
- [ ] Models têm created_at e updated_at
- [ ] Views protegidas com @login_required
- [ ] Dados filtrados por usuário
- [ ] Sem código comentado
- [ ] Sem prints de debug
- [ ] Imports organizados

---

## Troubleshooting

### Erro: "No module named 'django'"

**Solução**: Ativar ambiente virtual
```bash
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
```

### Erro: "Table doesn't exist"

**Solução**: Aplicar migrations
```bash
python manage.py migrate
```

### Erro: "Port already in use"

**Solução**: Usar porta diferente
```bash
python manage.py runserver 8001
```

Ou parar processo na porta 8000:
```bash
# Linux/Mac
lsof -ti:8000 | xargs kill -9

# Windows
netstat -ano | findstr :8000
taskkill /PID <pid> /F
```

### Erro: "CSRF token missing"

**Solução**: Adicionar {% csrf_token %} nos formulários
```django
<form method="post">
    {% csrf_token %}
    ...
</form>
```

---

## Deploy (Básico)

### Preparação

```bash
# 1. Definir DEBUG=False em produção
DEBUG = False

# 2. Configurar ALLOWED_HOSTS
ALLOWED_HOSTS = ['seudominio.com', 'www.seudominio.com']

# 3. Usar variáveis de ambiente para SECRET_KEY
SECRET_KEY = os.environ.get('SECRET_KEY')

# 4. Configurar banco de dados de produção (PostgreSQL recomendado)
DATABASES = {
    'default': dj_database_url.config(default=os.environ.get('DATABASE_URL'))
}

# 5. Configurar arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
```

### Checklist de Deploy

- [ ] DEBUG = False
- [ ] SECRET_KEY em variável de ambiente
- [ ] ALLOWED_HOSTS configurado
- [ ] Banco de dados de produção
- [ ] Arquivos estáticos coletados
- [ ] Migrations aplicadas
- [ ] Superusuário criado
- [ ] HTTPS configurado
- [ ] Backup strategy definida

---

## Recursos Adicionais

### Documentação Oficial
- Django: https://docs.djangoproject.com/
- TailwindCSS: https://tailwindcss.com/docs
- Python: https://docs.python.org/3/

### Ferramentas Recomendadas
- VS Code com extensões Python e Django
- DB Browser for SQLite (visualizar banco de dados)
- Postman (testar APIs, se aplicável)
- Git GUI (GitKraken, SourceTree)

### Comunidade
- Django Forum: https://forum.djangoproject.com/
- Stack Overflow: tag [django]
- Reddit: r/django

---

## Próximos Passos

Após configurar o ambiente:

1. Leia a [Arquitetura do Projeto](./architecture.md)
2. Revise os [Padrões de Código](./coding-standards.md)
3. Estude os [Modelos de Dados](./data-models.md)
4. Familiarize-se com o [Design System](./design-system.md)
5. Consulte o [PRD](../PRD.md) para entender os requisitos

Bom desenvolvimento!
