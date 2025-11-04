## Lista de Tarefas

### Sprint 0: Configuração Inicial do Projeto (Setup)

#### Tarefa 0.1: Configuração do Ambiente de Desenvolvimento
**Descrição**: Preparar ambiente local para desenvolvimento do projeto

**Subtarefas**:
- [X] 0.1.1: Criar diretório do projeto `finanpy`
- [X] 0.1.2: Criar ambiente virtual Python: `python -m venv venv`
- [X] 0.1.3: Ativar ambiente virtual
- [X] 0.1.4: Criar arquivo `requirements.txt` com dependências iniciais:
  ```
  Django==4.2.7
  python-decouple==3.8
  ```
- [X] 0.1.5: Instalar dependências: `pip install -r requirements.txt`
- [X] 0.1.6: Criar arquivo `.gitignore` com conteúdo padrão para Django:
  ```
  venv/
  __pycache__/
  *.pyc
  db.sqlite3
  .env
  *.log
  media/
  staticfiles/
  ```

#### Tarefa 0.2: Criação do Projeto Django
**Descrição**: Inicializar projeto Django e configurar estrutura base

**Subtarefas**:
- [X] 0.2.1: Criar projeto Django: `django-admin startproject core .`
- [X] 0.2.2: Renomear diretório do projeto de `core` para `core` se necessário
- [X] 0.2.3: Testar servidor de desenvolvimento: `python manage.py runserver`
- [X] 0.2.4: Verificar acesso em `http://localhost:8000`

#### Tarefa 0.3: Configuração de Settings
**Descrição**: Configurar arquivo settings.py com boas práticas

**Subtarefas**:
- [X] 0.3.1: Criar arquivo `.env` na raiz do projeto
- [X] 0.3.2: Mover SECRET_KEY para arquivo `.env`
- [X] 0.3.3: Configurar DEBUG através de variável de ambiente
- [X] 0.3.4: Configurar ALLOWED_HOSTS
- [X] 0.3.5: Adicionar configuração para usar aspas simples no código
- [X] 0.3.6: Configurar LANGUAGE_CODE = 'pt-br'
- [X] 0.3.7: Configurar TIME_ZONE = 'America/Sao_Paulo'
- [X] 0.3.8: Configurar USE_I18N = True
- [X] 0.3.9: Configurar USE_TZ = True

#### Tarefa 0.4: Criação de Apps Django
**Descrição**: Criar todos os apps necessários do projeto

**Subtarefas**:
- [X] 0.4.1: Criar app `users`: `python manage.py startapp users`
- [X] 0.4.2: Criar app `profiles`: `python manage.py startapp profiles`
- [X] 0.4.3: Criar app `accounts`: `python manage.py startapp accounts`
- [X] 0.4.4: Criar app `categories`: `python manage.py startapp categories`
- [X] 0.4.5: Criar app `transactions`: `python manage.py startapp transactions`
- [X] 0.4.6: Adicionar todos os apps em INSTALLED_APPS no settings.py:
  ```python
  INSTALLED_APPS = [
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
      'users',
      'profiles',
      'accounts',
      'categories',
      'transactions',
  ]
  ```

#### Tarefa 0.5: Configuração de TailwindCSS
**Descrição**: Integrar TailwindCSS ao projeto Django

**Subtarefas**:
- [X] 0.5.1: Instalar django-tailwind: adicionar `django-tailwind==3.8.0` ao requirements.txt
- [X] 0.5.2: Instalar dependência: `pip install django-tailwind`
- [X] 0.5.3: Adicionar 'tailwind' ao INSTALLED_APPS
- [X] 0.5.4: Executar: `python manage.py tailwind init`
- [X] 0.5.5: Adicionar app theme gerado ao INSTALLED_APPS
- [X] 0.5.6: Configurar TAILWIND_APP_NAME no settings.py
- [X] 0.5.7: Instalar dependências do Tailwind: `python manage.py tailwind install`
- [X] 0.5.8: Configurar NPM_BIN_PATH no settings.py se necessário

#### Tarefa 0.6: Estrutura de Templates e Static
**Descrição**: Criar estrutura de diretórios para templates e arquivos estáticos

**Subtarefas**:
- [X] 0.6.1: Criar diretório `templates` na raiz do projeto
- [X] 0.6.2: Criar diretório `static` na raiz do projeto
- [X] 0.6.3: Configurar TEMPLATES no settings.py para incluir diretório templates:
  ```python
  'DIRS': [BASE_DIR / 'templates'],
  ```
- [X] 0.6.4: Configurar STATIC_URL e STATICFILES_DIRS no settings.py:
  ```python
  STATIC_URL = '/static/'
  STATICFILES_DIRS = [BASE_DIR / 'static']
  ```
- [X] 0.6.5: Criar subdiretórios em templates: `templates/base/`, `templates/auth/`, etc.

#### Tarefa 0.7: Configuração Inicial do Git
**Descrição**: Inicializar repositório Git e fazer commit inicial

**Subtarefas**:
- [X] 0.7.1: Inicializar repositório Git: `git init`
- [X] 0.7.2: Verificar que .gitignore está configurado corretamente
- [X] 0.7.3: Adicionar arquivos: `git add .`
- [X] 0.7.4: Fazer commit inicial: `git commit -m "Initial project setup"`
- [X] 0.7.5: Criar arquivo README.md com informações básicas do projeto

---

### Sprint 1: Autenticação e Sistema de Usuários ✅ CONCLUÍDA

#### Tarefa 1.1: Model de Usuário Customizado
**Descrição**: Criar model customizado que herda de User do Django para permitir login com email

**Subtarefas**:
- [X] 1.1.1: Abrir arquivo `users/models.py`
- [X] 1.1.2: Importar AbstractUser e models do Django
- [X] 1.1.3: Criar classe CustomUser herdando de AbstractUser
- [X] 1.1.4: Definir campo email como único: `email = models.EmailField(unique=True)`
- [X] 1.1.5: Definir USERNAME_FIELD = 'email'
- [X] 1.1.6: Definir REQUIRED_FIELDS = []
- [X] 1.1.7: Adicionar campos created_at e updated_at
- [X] 1.1.8: Adicionar método __str__ retornando email
- [X] 1.1.9: Configurar AUTH_USER_MODEL = 'users.CustomUser' no settings.py
- [X] Tarefa 1.1 concluída

#### Tarefa 1.2: Configuração do Admin para CustomUser
**Descrição**: Configurar Django Admin para gerenciar usuários customizados

**Subtarefas**:
- [X] 1.2.1: Abrir arquivo `users/admin.py`
- [X] 1.2.2: Importar UserAdmin do Django
- [X] 1.2.3: Importar CustomUser model
- [X] 1.2.4: Criar classe CustomUserAdmin herdando de UserAdmin
- [X] 1.2.5: Configurar list_display com email, is_staff, is_active, date_joined
- [X] 1.2.6: Configurar ordering = ['email']
- [X] 1.2.7: Registrar CustomUser com CustomUserAdmin
- [X] Tarefa 1.2 concluída

#### Tarefa 1.3: Model de Profile
**Descrição**: Criar model de perfil de usuário com informações adicionais

**Subtarefas**:
- [X] 1.3.1: Abrir arquivo `profiles/models.py`
- [X] 1.3.2: Importar models e User (get_user_model)
- [X] 1.3.3: Criar classe Profile com campo OneToOneField para User
- [X] 1.3.4: Adicionar campo full_name (CharField, max_length=200, blank=True)
- [X] 1.3.5: Adicionar campo phone (CharField, max_length=20, blank=True)
- [X] 1.3.6: Adicionar campos created_at e updated_at
- [X] 1.3.7: Adicionar método __str__ retornando full_name ou email do usuário
- [X] 1.3.8: Adicionar Meta com verbose_name e verbose_name_plural
- [X] Tarefa 1.3 concluída

#### Tarefa 1.4: Signal para Criação Automática de Profile
**Descrição**: Implementar signal para criar perfil automaticamente ao criar usuário

**Subtarefas**:
- [X] 1.4.1: Criar arquivo `profiles/signals.py`
- [X] 1.4.2: Importar post_save signal e receiver decorator
- [X] 1.4.3: Importar User model (get_user_model)
- [X] 1.4.4: Importar Profile model
- [X] 1.4.5: Criar função create_profile com decorator @receiver(post_save, sender=User)
- [X] 1.4.6: Verificar if created e criar Profile.objects.create(user=instance)
- [X] 1.4.7: Abrir arquivo `profiles/apps.py`
- [X] 1.4.8: Override método ready() para importar signals
- [X] 1.4.9: Adicionar import de signals no método ready
- [X] Tarefa 1.4 concluída

#### Tarefa 1.5: Configuração do Admin para Profile
**Descrição**: Configurar Django Admin para gerenciar perfis

**Subtarefas**:
- [X] 1.5.1: Abrir arquivo `profiles/admin.py`
- [X] 1.5.2: Importar admin e Profile model
- [X] 1.5.3: Criar classe ProfileAdmin
- [X] 1.5.4: Configurar list_display com user email, full_name, phone
- [X] 1.5.5: Configurar search_fields com user email e full_name
- [X] 1.5.6: Registrar Profile com ProfileAdmin
- [X] Tarefa 1.5 concluída

#### Tarefa 1.6: Migrations Iniciais
**Descrição**: Criar e aplicar migrations para users e profiles

**Subtarefas**:
- [X] 1.6.1: Executar: `python manage.py makemigrations users`
- [X] 1.6.2: Verificar arquivo de migration gerado
- [X] 1.6.3: Executar: `python manage.py makemigrations profiles`
- [X] 1.6.4: Verificar arquivo de migration gerado
- [X] 1.6.5: Executar: `python manage.py migrate`
- [X] 1.6.6: Verificar que tabelas foram criadas no db.sqlite3
- [X] Tarefa 1.6 concluída

#### Tarefa 1.7: Template Base
**Descrição**: Criar template base com estrutura HTML e TailwindCSS

**Subtarefas**:
- [X] 1.7.1: Criar arquivo `templates/base.html`
- [X] 1.7.2: Adicionar DOCTYPE e estrutura HTML5 básica
- [X] 1.7.3: Adicionar tag {% load static %} e {% load tailwind_tags %}
- [X] 1.7.4: Adicionar {% tailwind_css %} no head
- [X] 1.7.5: Configurar meta tags (charset, viewport)
- [X] 1.7.6: Adicionar link para Google Fonts (Inter)
- [X] 1.7.7: Adicionar classe bg-bg-primary ao body
- [X] 1.7.8: Criar bloco {% block title %}
- [X] 1.7.9: Criar bloco {% block content %}
- [X] 1.7.10: Adicionar estrutura de mensagens do Django com estilização
- [X] Tarefa 1.7 concluída

#### Tarefa 1.8: View de Registro (Signup)
**Descrição**: Criar view para cadastro de novos usuários

**Subtarefas**:
- [X] 1.8.1: Criar arquivo `users/forms.py`
- [X] 1.8.2: Importar UserCreationForm e forms do Django
- [X] 1.8.3: Importar get_user_model
- [X] 1.8.4: Criar classe SignupForm herdando de UserCreationForm
- [X] 1.8.5: Adicionar campo email ao Meta.fields
- [X] 1.8.6: Configurar widgets com classes TailwindCSS
- [X] 1.8.7: Adicionar validação customizada para email único
- [X] 1.8.8: Abrir arquivo `users/views.py`
- [X] 1.8.9: Criar SignupView como CreateView
- [X] 1.8.10: Configurar form_class = SignupForm
- [X] 1.8.11: Configurar template_name = 'auth/signup.html'
- [X] 1.8.12: Configurar success_url para dashboard
- [X] 1.8.13: Override form_valid para fazer login automático após cadastro
- [X] Tarefa 1.8 concluída

#### Tarefa 1.9: Template de Registro
**Descrição**: Criar template HTML para página de cadastro

**Subtarefas**:
- [X] 1.9.1: Criar arquivo `templates/auth/signup.html`
- [X] 1.9.2: Extender base.html
- [X] 1.9.3: Adicionar título da página no block title
- [X] 1.9.4: Criar container centralizado com max-width
- [X] 1.9.5: Adicionar logo/nome Finanpy com gradiente
- [X] 1.9.6: Criar card com bg-bg-secondary e border
- [X] 1.9.7: Adicionar título "Criar Conta"
- [X] 1.9.8: Criar formulário com method POST e csrf_token
- [X] 1.9.9: Renderizar campos do form com classes TailwindCSS
- [X] 1.9.10: Adicionar botão de submit estilizado
- [X] 1.9.11: Adicionar link para página de login
- [X] 1.9.12: Adicionar tratamento de erros do formulário
- [X] Tarefa 1.9 concluída

#### Tarefa 1.10: View de Login
**Descrição**: Criar view para autenticação de usuários

**Subtarefas**:
- [X] 1.10.1: No arquivo `users/forms.py`, criar LoginForm
- [X] 1.10.2: Adicionar campo email (EmailField)
- [X] 1.10.3: Adicionar campo password (CharField com widget PasswordInput)
- [X] 1.10.4: Aplicar classes TailwindCSS aos widgets
- [X] 1.10.5: No arquivo `users/views.py`, criar LoginView como FormView
- [X] 1.10.6: Configurar form_class = LoginForm
- [X] 1.10.7: Configurar template_name = 'auth/login.html'
- [X] 1.10.8: Configurar success_url para dashboard
- [X] 1.10.9: Implementar método form_valid com authenticate e login
- [X] 1.10.10: Adicionar tratamento de credenciais inválidas
- [X] 1.10.11: Adicionar mensagem de erro para login inválido
- [X] Tarefa 1.10 concluída

#### Tarefa 1.11: Template de Login
**Descrição**: Criar template HTML para página de login

**Subtarefas**:
- [X] 1.11.1: Criar arquivo `templates/auth/login.html`
- [X] 1.11.2: Extender base.html
- [X] 1.11.3: Adicionar título da página
- [X] 1.11.4: Criar container centralizado
- [X] 1.11.5: Adicionar logo/nome Finanpy com gradiente
- [X] 1.11.6: Criar card de login estilizado
- [X] 1.11.7: Adicionar título "Entrar"
- [X] 1.11.8: Criar formulário de login
- [X] 1.11.9: Renderizar campos com estilização
- [X] 1.11.10: Adicionar botão de submit
- [X] 1.11.11: Adicionar link para página de cadastro
- [X] 1.11.12: Adicionar exibição de mensagens de erro
- [X] Tarefa 1.11 concluída

#### Tarefa 1.12: View de Logout
**Descrição**: Criar view para logout de usuários

**Subtarefas**:
- [X] 1.12.1: No arquivo `users/views.py`, importar LogoutView do Django
- [X] 1.12.2: Criar LogoutView personalizada se necessário
- [X] 1.12.3: Configurar LOGOUT_REDIRECT_URL = '/' no settings.py
- [X] 1.12.4: Adicionar mensagem de sucesso ao fazer logout
- [X] Tarefa 1.12 concluída

#### Tarefa 1.13: URLs de Autenticação
**Descrição**: Configurar URLs para views de autenticação

**Subtarefas**:
- [X] 1.13.1: Criar arquivo `users/urls.py`
- [X] 1.13.2: Importar path do Django
- [X] 1.13.3: Importar views de users
- [X] 1.13.4: Criar urlpatterns list
- [X] 1.13.5: Adicionar path para signup: path('signup/', SignupView.as_view(), name='signup')
- [X] 1.13.6: Adicionar path para login: path('login/', LoginView.as_view(), name='login')
- [X] 1.13.7: Adicionar path para logout: path('logout/', LogoutView.as_view(), name='logout')
- [X] 1.13.8: Abrir arquivo `core/urls.py`
- [X] 1.13.9: Adicionar include de users.urls: path('auth/', include('users.urls'))
- [X] Tarefa 1.13 concluída

#### Tarefa 1.14: Página Inicial Pública
**Descrição**: Criar página inicial para usuários não autenticados

**Subtarefas**:
- [X] 1.14.1: Criar arquivo `users/views.py` adicionar HomeView
- [X] 1.14.2: Criar TemplateView para home
- [X] 1.14.3: Configurar template_name = 'home.html'
- [X] 1.14.4: Override método get para redirecionar usuários autenticados
- [X] 1.14.5: Criar arquivo `templates/home.html`
- [X] 1.14.6: Extender base.html
- [X] 1.14.7: Criar seção hero com gradiente
- [X] 1.14.8: Adicionar logo e nome Finanpy
- [X] 1.14.9: Adicionar tagline/descrição do produto
- [X] 1.14.10: Adicionar botões de Cadastrar e Entrar estilizados
- [X] 1.14.11: Criar seção de features/funcionalidades
- [X] 1.14.12: Listar principais funcionalidades com ícones
- [X] 1.14.13: Adicionar URL no urls.py: path('', HomeView.as_view(), name='home')
- [X] Tarefa 1.14 concluída

#### Tarefa 1.15: Testes Manuais de Autenticação
**Descrição**: Testar fluxo completo de autenticação

**Subtarefas**:
- [X] 1.15.1: Iniciar servidor de desenvolvimento
- [X] 1.15.2: Acessar página inicial e verificar layout
- [X] 1.15.3: Clicar em "Cadastrar" e verificar redirecionamento
- [X] 1.15.4: Testar cadastro com email inválido
- [X] 1.15.5: Testar cadastro com senha fraca
- [X] 1.15.6: Cadastrar usuário válido
- [X] 1.15.7: Verificar redirecionamento após cadastro
- [X] 1.15.8: Fazer logout
- [X] 1.15.9: Tentar login com credenciais inválidas
- [X] 1.15.10: Fazer login com credenciais válidas
- [X] 1.15.11: Verificar que usuário autenticado é redirecionado da home
- [X] 1.15.12: Verificar criação automática do perfil no admin
- [X] Tarefa 1.15 concluída

---

### Sprint 2: Gestão de Contas Bancárias ✅ CONCLUÍDA

#### Tarefa 2.1: Model de Account ✅
**Descrição**: Criar model para representar contas bancárias do usuário

**Subtarefas**:
- [X] 2.1.1: Abrir arquivo `accounts/models.py`
- [X] 2.1.2: Importar models e get_user_model
- [X] 2.1.3: Criar classe Account com ForeignKey para User
- [X] 2.1.4: Adicionar campo name (CharField, max_length=100)
- [X] 2.1.5: Adicionar campo bank_name (CharField, max_length=100)
- [X] 2.1.6: Criar choices para account_type (CHECKING, SAVINGS, WALLET)
- [X] 2.1.7: Adicionar campo account_type com choices
- [X] 2.1.8: Adicionar campo balance (DecimalField, max_digits=12, decimal_places=2, default=0)
- [X] 2.1.9: Adicionar campo is_active (BooleanField, default=True)
- [X] 2.1.10: Adicionar campos created_at e updated_at
- [X] 2.1.11: Adicionar método __str__ retornando name
- [X] 2.1.12: Adicionar Meta com ordering, verbose_name e indexes

#### Tarefa 2.2: Admin de Account ✅
**Descrição**: Configurar Django Admin para gerenciar contas

**Subtarefas**:
- [X] 2.2.1: Abrir arquivo `accounts/admin.py`
- [X] 2.2.2: Importar admin e Account model
- [X] 2.2.3: Criar classe AccountAdmin
- [X] 2.2.4: Configurar list_display: user email, name, bank_name, account_type, balance, is_active
- [X] 2.2.5: Configurar list_filter: account_type, is_active
- [X] 2.2.6: Configurar search_fields: name, bank_name, user__email
- [X] 2.2.7: Configurar readonly_fields: created_at, updated_at
- [X] 2.2.8: Registrar Account com AccountAdmin

#### Tarefa 2.3: Form de Account ✅
**Descrição**: Criar formulário para cadastro e edição de contas

**Subtarefas**:
- [X] 2.3.1: Criar arquivo `accounts/forms.py`
- [X] 2.3.2: Importar forms e Account model
- [X] 2.3.3: Criar classe AccountForm herdando de forms.ModelForm
- [X] 2.3.4: Configurar Meta com model = Account
- [X] 2.3.5: Definir fields: name, bank_name, account_type, balance
- [X] 2.3.6: Configurar widgets com classes TailwindCSS para cada campo
- [X] 2.3.7: Adicionar labels em português para cada campo
- [X] 2.3.8: Adicionar placeholders nos widgets
- [X] 2.3.9: Configurar choices de account_type em português

#### Tarefa 2.4: View de Listagem de Contas ✅
**Descrição**: Criar view para listar contas do usuário

**Subtarefas**:
- [X] 2.4.1: Abrir arquivo `accounts/views.py`
- [X] 2.4.2: Importar LoginRequiredMixin e ListView
- [X] 2.4.3: Importar Account model
- [X] 2.4.4: Criar AccountListView herdando de LoginRequiredMixin e ListView
- [X] 2.4.5: Configurar model = Account
- [X] 2.4.6: Configurar template_name = 'accounts/account_list.html'
- [X] 2.4.7: Configurar context_object_name = 'accounts'
- [X] 2.4.8: Override get_queryset para filtrar por usuário: self.request.user
- [X] 2.4.9: Adicionar ordenação por nome
- [X] 2.4.10: Adicionar cálculo de saldo total no get_context_data

#### Tarefa 2.5: Template de Listagem de Contas ✅
**Descrição**: Criar template HTML para listar contas

**Subtarefas**:
- [X] 2.5.1: Criar arquivo `templates/accounts/account_list.html`
- [X] 2.5.2: Extender base.html
- [X] 2.5.3: Adicionar título "Minhas Contas"
- [X] 2.5.4: Criar header com título e botão "Nova Conta"
- [X] 2.5.5: Criar container com grid responsivo
- [X] 2.5.6: Iterar sobre accounts com for loop
- [X] 2.5.7: Para cada conta, criar card estilizado
- [X] 2.5.8: Exibir nome da conta em destaque
- [X] 2.5.9: Exibir nome do banco e tipo de conta
- [X] 2.5.10: Exibir saldo formatado com R$
- [X] 2.5.11: Adicionar botões de Editar e Excluir
- [X] 2.5.12: Adicionar mensagem quando não houver contas
- [X] 2.5.13: Adicionar card com saldo total consolidado

#### Tarefa 2.6: View de Criação de Conta ✅
**Descrição**: Criar view para cadastrar nova conta

**Subtarefas**:
- [X] 2.6.1: No arquivo `accounts/views.py`, importar CreateView
- [X] 2.6.2: Importar AccountForm
- [X] 2.6.3: Criar AccountCreateView herdando de LoginRequiredMixin e CreateView
- [X] 2.6.4: Configurar model = Account
- [X] 2.6.5: Configurar form_class = AccountForm
- [X] 2.6.6: Configurar template_name = 'accounts/account_form.html'
- [X] 2.6.7: Configurar success_url para lista de contas
- [X] 2.6.8: Override form_valid para associar user: form.instance.user = self.request.user
- [X] 2.6.9: Adicionar mensagem de sucesso
- [X] 2.6.10: Adicionar context extra com título da página

#### Tarefa 2.7: View de Edição de Conta ✅
**Descrição**: Criar view para editar conta existente

**Subtarefas**:
- [X] 2.7.1: No arquivo `accounts/views.py`, importar UpdateView
- [X] 2.7.2: Criar AccountUpdateView herdando de LoginRequiredMixin e UpdateView
- [X] 2.7.3: Configurar model, form_class e template_name
- [X] 2.7.4: Configurar success_url
- [X] 2.7.5: Override get_queryset para filtrar por usuário
- [X] 2.7.6: Adicionar mensagem de sucesso
- [X] 2.7.7: Adicionar context extra com título

#### Tarefa 2.8: View de Exclusão de Conta ✅
**Descrição**: Criar view para excluir conta

**Subtarefas**:
- [X] 2.8.1: No arquivo `accounts/views.py`, importar DeleteView
- [X] 2.8.2: Criar AccountDeleteView herdando de LoginRequiredMixin e DeleteView
- [X] 2.8.3: Configurar model = Account
- [X] 2.8.4: Configurar template_name = 'accounts/account_confirm_delete.html'
- [X] 2.8.5: Configurar success_url para lista de contas
- [X] 2.8.6: Override get_queryset para filtrar por usuário
- [X] 2.8.7: Adicionar mensagem de sucesso
- [X] 2.8.8: Adicionar validação para não excluir conta com transações (implementar depois)

#### Tarefa 2.9: Template de Form de Conta ✅
**Descrição**: Criar template HTML para criar/editar conta

**Subtarefas**:
- [X] 2.9.1: Criar arquivo `templates/accounts/account_form.html`
- [X] 2.9.2: Extender base.html
- [X] 2.9.3: Adicionar título dinâmico (Nova Conta ou Editar Conta)
- [X] 2.9.4: Criar container centralizado
- [X] 2.9.5: Criar card com formulário
- [X] 2.9.6: Adicionar form com method POST e csrf_token
- [X] 2.9.7: Renderizar campos do form com {{ form.as_p }} ou manualmente
- [X] 2.9.8: Estilizar cada campo individualmente com TailwindCSS
- [X] 2.9.9: Adicionar botão de Salvar
- [X] 2.9.10: Adicionar botão de Cancelar
- [X] 2.9.11: Adicionar exibição de erros do formulário

#### Tarefa 2.10: Template de Confirmação de Exclusão ✅
**Descrição**: Criar template para confirmar exclusão de conta

**Subtarefas**:
- [X] 2.10.1: Criar arquivo `templates/accounts/account_confirm_delete.html`
- [X] 2.10.2: Extender base.html
- [X] 2.10.3: Adicionar título "Confirmar Exclusão"
- [X] 2.10.4: Criar card com mensagem de confirmação
- [X] 2.10.5: Exibir nome da conta a ser excluída
- [X] 2.10.6: Adicionar aviso sobre exclusão permanente
- [X] 2.10.7: Criar form com method POST e csrf_token
- [X] 2.10.8: Adicionar botão de Confirmar Exclusão (vermelho)
- [X] 2.10.9: Adicionar botão de Cancelar
- [X] 2.10.10: Estilizar com cores de alerta

#### Tarefa 2.11: URLs de Accounts ✅
**Descrição**: Configurar URLs para views de contas

**Subtarefas**:
- [X] 2.11.1: Criar arquivo `accounts/urls.py`
- [X] 2.11.2: Importar path e views
- [X] 2.11.3: Criar urlpatterns list
- [X] 2.11.4: Adicionar path para list: path('', AccountListView.as_view(), name='account_list')
- [X] 2.11.5: Adicionar path para create: path('new/', AccountCreateView.as_view(), name='account_create')
- [X] 2.11.6: Adicionar path para update: path('<int:pk>/edit/', AccountUpdateView.as_view(), name='account_update')
- [X] 2.11.7: Adicionar path para delete: path('<int:pk>/delete/', AccountDeleteView.as_view(), name='account_delete')
- [X] 2.11.8: No arquivo `core/urls.py`, incluir accounts.urls: path('accounts/', include('accounts.urls'))

#### Tarefa 2.12: Migration de Account ✅
**Descrição**: Criar e aplicar migration para model Account

**Subtarefas**:
- [X] 2.12.1: Executar: `python manage.py makemigrations accounts`
- [X] 2.12.2: Verificar arquivo de migration gerado
- [X] 2.12.3: Executar: `python manage.py migrate`
- [X] 2.12.4: Verificar tabela no banco de dados

#### Tarefa 2.13: Testes Manuais de Accounts ✅
**Descrição**: Testar CRUD completo de contas

**Subtarefas**:
- [X] 2.13.1: Fazer login no sistema
- [X] 2.13.2: Acessar página de contas
- [X] 2.13.3: Verificar mensagem de lista vazia
- [X] 2.13.4: Criar nova conta corrente
- [X] 2.13.5: Verificar redirecionamento e mensagem de sucesso
- [X] 2.13.6: Criar conta poupança
- [X] 2.13.7: Criar conta tipo carteira
- [X] 2.13.8: Verificar que todas as contas aparecem na listagem
- [X] 2.13.9: Editar nome de uma conta
- [X] 2.13.10: Editar saldo de uma conta
- [X] 2.13.11: Tentar excluir uma conta
- [X] 2.13.12: Verificar que conta foi excluída
- [X] 2.13.13: Verificar que outro usuário não vê as contas
- [X] 2.13.14: Verificar cálculo de saldo total

- [X] Tarefa 2.13 concluída

---

### Sprint 3: Gestão de Categorias ✅ CONCLUÍDA

#### Tarefa 3.1: Model de Category
**Descrição**: Criar model para categorias de transações

**Subtarefas**:
- [X] 3.1.1: Abrir arquivo `categories/models.py`
- [X] 3.1.2: Importar models e get_user_model
- [X] 3.1.3: Criar classe Category com ForeignKey para User
- [X] 3.1.4: Adicionar campo name (CharField, max_length=50)
- [X] 3.1.5: Criar choices para category_type (INCOME, EXPENSE)
- [X] 3.1.6: Adicionar campo category_type com choices
- [X] 3.1.7: Adicionar campo color (CharField, max_length=7, default='#667eea')
- [X] 3.1.8: Adicionar campos created_at e updated_at
- [X] 3.1.9: Adicionar método __str__ retornando name
- [X] 3.1.10: Adicionar Meta com ordering e verbose_name
- [X] 3.1.11: Adicionar unique_together para (user, name)

#### Tarefa 3.2: Admin de Category
**Descrição**: Configurar Django Admin para categorias

**Subtarefas**:
- [X] 3.2.1: Abrir arquivo `categories/admin.py`
- [X] 3.2.2: Importar admin e Category model
- [X] 3.2.3: Criar classe CategoryAdmin
- [X] 3.2.4: Configurar list_display: user email, name, category_type, color
- [X] 3.2.5: Configurar list_filter: category_type
- [X] 3.2.6: Configurar search_fields: name, user__email
- [X] 3.2.7: Configurar readonly_fields: created_at, updated_at
- [X] 3.2.8: Registrar Category com CategoryAdmin

#### Tarefa 3.3: Form de Category
**Descrição**: Criar formulário para categorias

**Subtarefas**:
- [X] 3.3.1: Criar arquivo `categories/forms.py`
- [X] 3.3.2: Importar forms e Category model
- [X] 3.3.3: Criar CategoryForm herdando de forms.ModelForm
- [X] 3.3.4: Configurar Meta com model e fields
- [X] 3.3.5: Definir fields: name, category_type, color
- [X] 3.3.6: Configurar widgets com classes TailwindCSS
- [X] 3.3.7: Usar input type color para campo color
- [X] 3.3.8: Adicionar labels em português
- [X] 3.3.9: Adicionar placeholders
- [X] 3.3.10: Traduzir choices para português

#### Tarefa 3.4: View de Listagem de Categorias
**Descrição**: Criar view para listar categorias

**Subtarefas**:
- [X] 3.4.1: Abrir arquivo `categories/views.py`
- [X] 3.4.2: Importar LoginRequiredMixin e ListView
- [X] 3.4.3: Importar Category model
- [X] 3.4.4: Criar CategoryListView
- [X] 3.4.5: Configurar model, template_name e context_object_name
- [X] 3.4.6: Override get_queryset para filtrar por usuário
- [X] 3.4.7: Adicionar ordenação por categoria_type e name
- [X] 3.4.8: Adicionar separação de categorias de entrada e saída no context

#### Tarefa 3.5: Template de Listagem de Categorias
**Descrição**: Criar template para listar categorias

**Subtarefas**:
- [X] 3.5.1: Criar arquivo `templates/categories/category_list.html`
- [X] 3.5.2: Extender base.html
- [X] 3.5.3: Adicionar título "Minhas Categorias"
- [X] 3.5.4: Criar header com botão "Nova Categoria"
- [X] 3.5.5: Criar duas seções: Entradas e Saídas
- [X] 3.5.6: Iterar sobre categorias de entrada
- [X] 3.5.7: Para cada categoria, criar badge com nome e cor
- [X] 3.5.8: Adicionar botões de Editar e Excluir
- [X] 3.5.9: Repetir para categorias de saída
- [X] 3.5.10: Adicionar mensagem quando não houver categorias
- [X] 3.5.11: Usar cores diferentes para entrada (verde) e saída (vermelho)

#### Tarefa 3.6: View de Criação de Categoria
**Descrição**: Criar view para cadastrar categoria

**Subtarefas**:
- [X] 3.6.1: No `categories/views.py`, importar CreateView
- [X] 3.6.2: Importar CategoryForm
- [X] 3.6.3: Criar CategoryCreateView
- [X] 3.6.4: Configurar model, form_class e template_name
- [X] 3.6.5: Configurar success_url
- [X] 3.6.6: Override form_valid para associar usuário
- [X] 3.6.7: Adicionar mensagem de sucesso
- [X] 3.6.8: Adicionar tratamento de erro para nome duplicado

#### Tarefa 3.7: View de Edição de Categoria
**Descrição**: Criar view para editar categoria

**Subtarefas**:
- [X] 3.7.1: No `categories/views.py`, importar UpdateView
- [X] 3.7.2: Criar CategoryUpdateView
- [X] 3.7.3: Configurar atributos necessários
- [X] 3.7.4: Override get_queryset para filtrar por usuário
- [X] 3.7.5: Adicionar mensagem de sucesso

#### Tarefa 3.8: View de Exclusão de Categoria
**Descrição**: Criar view para excluir categoria

**Subtarefas**:
- [X] 3.8.1: No `categories/views.py`, importar DeleteView
- [X] 3.8.2: Criar CategoryDeleteView
- [X] 3.8.3: Configurar atributos necessários
- [X] 3.8.4: Override get_queryset
- [X] 3.8.5: Adicionar mensagem de sucesso
- [X] 3.8.6: Adicionar validação para não excluir categoria com transações

#### Tarefa 3.9: Templates de Form e Delete de Categoria
**Descrição**: Criar templates para forms de categoria

**Subtarefas**:
- [X] 3.9.1: Criar `templates/categories/category_form.html`
- [X] 3.9.2: Extender base e criar formulário estilizado
- [X] 3.9.3: Adicionar preview da cor selecionada
- [X] 3.9.4: Adicionar botões de ação
- [X] 3.9.5: Criar `templates/categories/category_confirm_delete.html`
- [X] 3.9.6: Adicionar mensagem de confirmação
- [X] 3.9.7: Estilizar com cores de alerta

#### Tarefa 3.10: URLs de Categories
**Descrição**: Configurar URLs para views de categorias

**Subtarefas**:
- [X] 3.10.1: Criar arquivo `categories/urls.py`
- [X] 3.10.2: Adicionar paths para todas as views
- [X] 3.10.3: Incluir no `core/urls.py`

#### Tarefa 3.11: Migration de Category
**Descrição**: Criar e aplicar migrations

**Subtarefas**:
- [X] 3.11.1: Executar makemigrations
- [X] 3.11.2: Verificar migration
- [X] 3.11.3: Executar migrate
- [X] 3.11.4: Verificar no banco

#### Tarefa 3.12: Categorias Padrão
**Descrição**: Criar signal para adicionar categorias padrão ao novo usuário

**Subtarefas**:
- [X] 3.12.1: Criar arquivo `categories/signals.py`
- [X] 3.12.2: Criar função para criar categorias padrão
- [X] 3.12.3: Definir lista de categorias padrão (Salário, Alimentação, Transporte, etc)
- [X] 3.12.4: Conectar ao signal post_save de User
- [X] 3.12.5: Importar signals no apps.py
- [X] 3.12.6: Testar criação automática

#### Tarefa 3.13: Testes Manuais de Categories ✅
**Descrição**: Testar CRUD de categorias

**Subtarefas**:
- [X] 3.13.1: Fazer login
- [X] 3.13.2: Acessar página de categorias
- [X] 3.13.3: Verificar categorias padrão criadas
- [X] 3.13.4: Criar categoria de entrada personalizada
- [X] 3.13.5: Criar categoria de saída personalizada
- [X] 3.13.6: Testar seletor de cor
- [X] 3.13.7: Editar categoria
- [X] 3.13.8: Tentar criar categoria com nome duplicado
- [X] 3.13.9: Excluir categoria
- [X] 3.13.10: Verificar separação visual entre entradas e saídas

---

### Sprint 4: Gestão de Transações ✅ CONCLUÍDA

#### Tarefa 4.1: Model de Transaction
**Descrição**: Criar model para transações financeiras

**Subtarefas**:
- [X] 4.1.1: Abrir arquivo `transactions/models.py`
- [X] 4.1.2: Importar models, Account e Category
- [X] 4.1.3: Criar classe Transaction
- [X] 4.1.4: Adicionar ForeignKey para Account (on_delete=PROTECT)
- [X] 4.1.5: Adicionar ForeignKey para Category (on_delete=PROTECT)
- [X] 4.1.6: Criar choices para transaction_type (INCOME, EXPENSE)
- [X] 4.1.7: Adicionar campo transaction_type
- [X] 4.1.8: Adicionar campo amount (DecimalField, max_digits=12, decimal_places=2)
- [X] 4.1.9: Adicionar campo transaction_date (DateField)
- [X] 4.1.10: Adicionar campo description (TextField, blank=True)
- [X] 4.1.11: Adicionar created_at e updated_at
- [X] 4.1.12: Adicionar método __str__
- [X] 4.1.13: Adicionar Meta com ordering por -transaction_date
- [X] Tarefa 4.1 concluída

#### Tarefa 4.2: Signal para Atualização de Saldo
**Descrição**: Criar signals para atualizar saldo da conta automaticamente

**Subtarefas**:
- [X] 4.2.1: Criar arquivo `transactions/signals.py`
- [X] 4.2.2: Importar post_save, post_delete, pre_save
- [X] 4.2.3: Criar função update_balance_on_create
- [X] 4.2.4: Conectar ao post_save de Transaction
- [X] 4.2.5: Implementar lógica: se INCOME adiciona, se EXPENSE subtrai
- [X] 4.2.6: Criar função update_balance_on_delete
- [X] 4.2.7: Implementar lógica reversa ao excluir
- [X] 4.2.8: Criar função update_balance_on_update usando pre_save
- [X] 4.2.9: Salvar valores antigos antes de atualizar
- [X] 4.2.10: Recalcular saldo considerando mudanças
- [X] 4.2.11: Importar signals no apps.py
- [X] 4.2.12: Adicionar tratamento de erros
- [X] Tarefa 4.2 concluída

#### Tarefa 4.3: Admin de Transaction
**Descrição**: Configurar Django Admin para transações

**Subtarefas**:
- [X] 4.3.1: Abrir arquivo `transactions/admin.py`
- [X] 4.3.2: Criar TransactionAdmin
- [X] 4.3.3: Configurar list_display: transaction_date, description, account, category, transaction_type, amount
- [X] 4.3.4: Configurar list_filter: transaction_type, transaction_date, category
- [X] 4.3.5: Configurar search_fields: description, account__name
- [X] 4.3.6: Configurar date_hierarchy: transaction_date
- [X] 4.3.7: Configurar readonly_fields: created_at, updated_at
- [X] 4.3.8: Registrar Transaction
- [X] Tarefa 4.3 concluída

#### Tarefa 4.4: Form de Transaction
**Descrição**: Criar formulário para transações

**Subtarefas**:
- [X] 4.4.1: Criar arquivo `transactions/forms.py`
- [X] 4.4.2: Criar TransactionForm
- [X] 4.4.3: Definir fields: account, category, transaction_type, amount, transaction_date, description
- [X] 4.4.4: Configurar widgets com TailwindCSS
- [X] 4.4.5: Usar DateInput com type='date'
- [X] 4.4.6: Adicionar labels em português
- [X] 4.4.7: Adicionar placeholders
- [X] 4.4.8: Adicionar método __init__ para filtrar accounts e categories do usuário
- [X] 4.4.9: Adicionar validação: category_type deve corresponder a transaction_type
- [X] 4.4.10: Adicionar validação: amount deve ser positivo
- [X] Tarefa 4.4 concluída

#### Tarefa 4.5: View de Listagem de Transações
**Descrição**: Criar view para listar transações com filtros

**Subtarefas**:
- [X] 4.5.1: Abrir `transactions/views.py`
- [X] 4.5.2: Importar ListView e Transaction
- [X] 4.5.3: Criar TransactionListView
- [X] 4.5.4: Override get_queryset para filtrar por usuário (via account__user)
- [X] 4.5.5: Implementar filtros por data_inicio, data_fim (GET params)
- [X] 4.5.6: Implementar filtro por conta (GET param)
- [X] 4.5.7: Implementar filtro por categoria (GET param)
- [X] 4.5.8: Adicionar paginação (paginate_by = 20)
- [X] 4.5.9: Adicionar estatísticas no context: total_income, total_expense, balance
- [X] 4.5.10: Passar contas e categorias do usuário para o context (para filtros)
- [X] Tarefa 4.5 concluída

#### Tarefa 4.6: Template de Listagem de Transações
**Descrição**: Criar template para listar transações

**Subtarefas**:
- [X] 4.6.1: Criar `templates/transactions/transaction_list.html`
- [X] 4.6.2: Extender base.html
- [X] 4.6.3: Criar header com título e botão "Nova Transação"
- [X] 4.6.4: Criar seção de filtros com formulário GET
- [X] 4.6.5: Adicionar inputs para data início e fim
- [X] 4.6.6: Adicionar select para conta
- [X] 4.6.7: Adicionar select para categoria
- [X] 4.6.8: Adicionar botão "Filtrar" e "Limpar Filtros"
- [X] 4.6.9: Criar seção de cards com estatísticas (Total Entradas, Total Saídas, Balanço)
- [X] 4.6.10: Criar tabela responsiva para transações
- [X] 4.6.11: Colunas: Data, Descrição, Conta, Categoria, Tipo, Valor, Ações
- [X] 4.6.12: Usar cores diferentes para INCOME (verde) e EXPENSE (vermelho)
- [X] 4.6.13: Adicionar botões Editar e Excluir
- [X] 4.6.14: Adicionar paginação
- [X] 4.6.15: Adicionar mensagem quando lista vazia
- [X] Tarefa 4.6 concluída

#### Tarefa 4.7: View de Criação de Transação
**Descrição**: Criar view para registrar nova transação

**Subtarefas**:
- [X] 4.7.1: No `transactions/views.py`, criar TransactionCreateView
- [X] 4.7.2: Configurar form_class = TransactionForm
- [X] 4.7.3: Configurar template e success_url
- [X] 4.7.4: Override get_form_kwargs para passar request.user ao form
- [X] 4.7.5: Adicionar mensagem de sucesso
- [X] 4.7.6: Adicionar tratamento de erro
- [X] Tarefa 4.7 concluída

#### Tarefa 4.8: View de Edição de Transação
**Descrição**: Criar view para editar transação

**Subtarefas**:
- [X] 4.8.1: Criar TransactionUpdateView
- [X] 4.8.2: Configurar atributos necessários
- [X] 4.8.3: Override get_queryset para filtrar por usuário
- [X] 4.8.4: Override get_form_kwargs
- [X] 4.8.5: Adicionar mensagem de sucesso
- [X] Tarefa 4.8 concluída

#### Tarefa 4.9: View de Exclusão de Transação
**Descrição**: Criar view para excluir transação

**Subtarefas**:
- [X] 4.9.1: Criar TransactionDeleteView
- [X] 4.9.2: Configurar atributos
- [X] 4.9.3: Override get_queryset
- [X] 4.9.4: Adicionar mensagem de sucesso
- [X] Tarefa 4.9 concluída

#### Tarefa 4.10: Templates de Form e Delete
**Descrição**: Criar templates para forms de transação

**Subtarefas**:
- [X] 4.10.1: Criar `templates/transactions/transaction_form.html`
- [X] 4.10.2: Criar formulário estilizado
- [X] 4.10.3: Adicionar JavaScript para filtrar categorias baseado no tipo
- [X] 4.10.4: Criar `templates/transactions/transaction_confirm_delete.html`
- [X] 4.10.5: Adicionar informações da transação
- [X] 4.10.6: Adicionar aviso sobre atualização de saldo
- [X] Tarefa 4.10 concluída

#### Tarefa 4.11: URLs de Transactions
**Descrição**: Configurar URLs para transações

**Subtarefas**:
- [X] 4.11.1: Criar `transactions/urls.py`
- [X] 4.11.2: Adicionar paths para list, create, update, delete
- [X] 4.11.3: Incluir no `core/urls.py`
- [X] Tarefa 4.11 concluída

#### Tarefa 4.12: Migration de Transaction
**Descrição**: Criar e aplicar migrations

**Subtarefas**:
- [X] 4.12.1: Executar makemigrations
- [X] 4.12.2: Revisar migration
- [X] 4.12.3: Executar migrate
- [X] 4.12.4: Verificar tabela
- [X] Tarefa 4.12 concluída

#### Tarefa 4.13: Testes Manuais de Transactions
**Descrição**: Testar funcionalidades de transações

**Subtarefas**:
- [X] 4.13.1: Criar transação de entrada
- [X] 4.13.2: Verificar atualização de saldo da conta
- [X] 4.13.3: Criar transação de saída
- [X] 4.13.4: Verificar subtração do saldo
- [X] 4.13.5: Editar transação e verificar recálculo
- [X] 4.13.6: Excluir transação e verificar reversão do saldo
- [X] 4.13.7: Testar filtros por data
- [X] 4.13.8: Testar filtros por conta
- [X] 4.13.9: Testar filtros por categoria
- [X] 4.13.10: Testar combinação de filtros
- [X] 4.13.11: Verificar cálculo de estatísticas
- [X] 4.13.12: Testar paginação
- [X] 4.13.13: Testar validação de categoria vs tipo
- [X] 4.13.14: Verificar que usuário só vê suas transações
- [X] Tarefa 4.13 concluída

---

### Sprint 5: Dashboard e Visualizações ✅ CONCLUÍDA

#### Tarefa 5.1: View do Dashboard
**Descrição**: Criar view principal do dashboard com estatísticas

**Subtarefas**:
- [X] 5.1.1: Criar arquivo `users/views.py` (ou usar existente)
- [X] 5.1.2: Importar TemplateView e modelos necessários
- [X] 5.1.3: Criar DashboardView herdando de LoginRequiredMixin e TemplateView
- [X] 5.1.4: Configurar template_name = 'dashboard.html'
- [X] 5.1.5: Override get_context_data
- [X] 5.1.6: Calcular saldo total de todas as contas do usuário
- [X] 5.1.7: Calcular total de entradas do mês atual
- [X] 5.1.8: Calcular total de saídas do mês atual
- [X] 5.1.9: Calcular balanço do mês (entradas - saídas)
- [X] 5.1.10: Buscar últimas 10 transações do usuário
- [X] 5.1.11: Calcular totais por categoria do mês
- [X] 5.1.12: Contar número de contas ativas
- [X] 5.1.13: Adicionar todos os dados ao context

#### Tarefa 5.2: Template do Dashboard
**Descrição**: Criar template HTML do dashboard principal

**Subtarefas**:
- [X] 5.2.1: Criar arquivo `templates/dashboard.html`
- [X] 5.2.2: Extender base.html
- [X] 5.2.3: Adicionar título "Dashboard"
- [X] 5.2.4: Criar seção de boas-vindas com nome do usuário
- [X] 5.2.5: Criar grid com 4 cards de estatísticas principais
- [X] 5.2.6: Card 1: Saldo Total (gradiente primário)
- [X] 5.2.7: Card 2: Entradas do Mês (verde)
- [X] 5.2.8: Card 3: Saídas do Mês (vermelho)
- [X] 5.2.9: Card 4: Balanço do Mês (azul se positivo, vermelho se negativo)
- [X] 5.2.10: Criar seção "Ações Rápidas" com botões
- [X] 5.2.11: Botão para Nova Transação
- [X] 5.2.12: Botão para Nova Conta
- [X] 5.2.13: Botão para Nova Categoria
- [X] 5.2.14: Criar seção "Transações Recentes"
- [X] 5.2.15: Listar últimas transações em tabela compacta
- [X] 5.2.16: Link "Ver Todas" para página de transações
- [X] 5.2.17: Criar seção "Gastos por Categoria"
- [X] 5.2.18: Exibir top 5 categorias do mês com barras de progresso
- [X] 5.2.19: Usar cores das categorias
- [X] 5.2.20: Adicionar responsividade mobile-first

#### Tarefa 5.3: Menu de Navegação Principal
**Descrição**: Criar componente de navegação consistente

**Subtarefas**:
- [X] 5.3.1: Criar arquivo `templates/includes/navbar.html`
- [X] 5.3.2: Criar estrutura de navbar com TailwindCSS
- [X] 5.3.3: Adicionar logo/nome Finanpy à esquerda
- [X] 5.3.4: Adicionar links de navegação no centro
- [X] 5.3.5: Link para Dashboard
- [X] 5.3.6: Link para Contas
- [X] 5.3.7: Link para Categorias
- [X] 5.3.8: Link para Transações
- [X] 5.3.9: Adicionar dropdown de usuário à direita
- [X] 5.3.10: Exibir nome/email do usuário
- [X] 5.3.11: Link para Ver Perfil
- [X] 5.3.12: Link para Editar Perfil
- [X] 5.3.13: Botão de Logout
- [X] 5.3.14: Adicionar indicador de página ativa
- [X] 5.3.15: Implementar menu hambúrguer para mobile
- [X] 5.3.16: Incluir navbar no base.html

#### Tarefa 5.4: Visualização de Perfil
**Descrição**: Criar página para visualizar dados do perfil

**Subtarefas**:
- [X] 5.4.1: No `profiles/views.py`, criar ProfileDetailView
- [X] 5.4.2: Configurar para buscar perfil do usuário logado
- [X] 5.4.3: Configurar template_name
- [X] 5.4.4: Criar `templates/profiles/profile_detail.html`
- [X] 5.4.5: Exibir foto placeholder (círculo com iniciais)
- [X] 5.4.6: Exibir nome completo
- [X] 5.4.7: Exibir email (não editável)
- [X] 5.4.8: Exibir telefone
- [X] 5.4.9: Exibir data de cadastro
- [X] 5.4.10: Adicionar botão "Editar Perfil"
- [X] 5.4.11: Criar design com cards estilizados

#### Tarefa 5.5: Edição de Perfil
**Descrição**: Criar formulário para editar perfil

**Subtarefas**:
- [X] 5.5.1: Criar `profiles/forms.py`
- [X] 5.5.2: Criar ProfileForm
- [X] 5.5.3: Incluir fields: full_name, phone
- [X] 5.5.4: Aplicar widgets com TailwindCSS
- [X] 5.5.5: Adicionar labels e placeholders em português
- [X] 5.5.6: No `profiles/views.py`, criar ProfileUpdateView
- [X] 5.5.7: Configurar para editar perfil do usuário logado
- [X] 5.5.8: Criar `templates/profiles/profile_form.html`
- [X] 5.5.9: Criar formulário estilizado
- [X] 5.5.10: Adicionar botões Salvar e Cancelar

#### Tarefa 5.6: URLs de Dashboard e Profile
**Descrição**: Configurar URLs para dashboard e perfil

**Subtarefas**:
- [X] 5.6.1: Criar `profiles/urls.py`
- [X] 5.6.2: Adicionar paths para profile detail e update
- [X] 5.6.3: Incluir no `core/urls.py`
- [X] 5.6.4: Adicionar URL do dashboard no `core/urls.py`
- [X] 5.6.5: Configurar LOGIN_REDIRECT_URL = '/dashboard/' no settings.py

#### Tarefa 5.7: Formatação de Valores Monetários
**Descrição**: Criar template tags para formatar valores em reais

**Subtarefas**:
- [X] 5.7.1: Criar diretório `users/templatetags/`
- [X] 5.7.2: Criar arquivo `__init__.py`
- [X] 5.7.3: Criar arquivo `currency_filters.py`
- [X] 5.7.4: Criar filtro currency para formatar em R$
- [X] 5.7.5: Usar locale pt_BR
- [X] 5.7.6: Testar formatação em templates
- [X] 5.7.7: Aplicar em todos os templates que exibem valores

#### Tarefa 5.8: Mensagens de Feedback
**Descrição**: Padronizar sistema de mensagens do Django

**Subtarefas**:
- [X] 5.8.1: No base.html, criar seção para mensagens
- [X] 5.8.2: Estilizar mensagens de sucesso (verde)
- [X] 5.8.3: Estilizar mensagens de erro (vermelho)
- [X] 5.8.4: Estilizar mensagens de aviso (amarelo)
- [X] 5.8.5: Estilizar mensagens de info (azul)
- [X] 5.8.6: Adicionar botão para fechar mensagens
- [X] 5.8.7: Adicionar auto-dismiss com JavaScript (opcional)
- [X] 5.8.8: Testar em todas as views

#### Tarefa 5.9: Melhorias de UX
**Descrição**: Implementar melhorias de experiência do usuário

**Subtarefas**:
- [X] 5.9.1: Adicionar breadcrumbs nas páginas internas
- [X] 5.9.2: Adicionar título da página no navegador (tag title)
- [X] 5.9.3: Adicionar confirmação JavaScript para exclusões
- [X] 5.9.4: Adicionar loading states em botões (opcional)
- [X] 5.9.5: Melhorar responsividade em mobile
- [X] 5.9.6: Adicionar tooltips onde necessário
- [X] 5.9.7: Padronizar espaçamentos
- [X] 5.9.8: Adicionar animações suaves (transitions)

#### Tarefa 5.10: Testes Manuais Completos
**Descrição**: Testar fluxo completo da aplicação

**Subtarefas**:
- [X] 5.10.1: Testar cadastro de novo usuário
- [X] 5.10.2: Verificar criação automática de perfil e categorias
- [X] 5.10.3: Navegar pelo dashboard
- [X] 5.10.4: Criar contas, categorias e transações
- [X] 5.10.5: Verificar cálculos no dashboard
- [X] 5.10.6: Testar filtros de transações
- [X] 5.10.7: Editar perfil
- [X] 5.10.8: Testar navegação entre páginas
- [X] 5.10.9: Testar responsividade mobile
- [X] 5.10.10: Verificar mensagens de feedback
- [X] 5.10.11: Testar logout e login novamente
- [X] 5.10.12: Verificar isolamento de dados entre usuários

---

### Sprint 6: Refinamentos e Otimizações

#### Tarefa 6.1: Validações Adicionais
**Descrição**: Implementar validações de negócio adicionais

**Subtarefas**:
- [X] 6.1.1: Validar que não é possível excluir conta com transações
- [X] 6.1.2: Validar que não é possível excluir categoria com transações
- [X] 6.1.3: Adicionar validação de data no futuro para transações
- [X] 6.1.4: Validar valores negativos
- [X] 6.1.5: Adicionar validação de saldo suficiente (opcional)
- [X] 6.1.6: Testar todas as validações

#### Tarefa 6.2: Ordenação e Paginação ✅
**Descrição**: Melhorar ordenação e adicionar paginação onde necessário

**Subtarefas**:
- [X] 6.2.1: Adicionar ordenação clicável em tabelas
- [X] 6.2.2: Implementar paginação em lista de contas
- [X] 6.2.3: Melhorar paginação de transações
- [X] 6.2.4: Adicionar "Mostrar X por página"
- [X] 6.2.5: Estilizar componentes de paginação

#### Tarefa 6.3: Busca e Filtros Avançados ✅
**Descrição**: Implementar funcionalidades de busca

**Subtarefas**:
- [X] 6.3.1: Adicionar campo de busca em transações (descrição)
- [X] 6.3.2: Adicionar filtro por status ativo em contas
- [X] 6.3.3: Implementar busca em categorias
- [X] 6.3.4: Adicionar filtros rápidos (Este Mês, Último Mês, etc)
- [X] 6.3.5: Salvar filtros em query string

#### Tarefa 6.4: Gráficos e Visualizações (Opcional) ✅
**Descrição**: Adicionar gráficos simples usando Chart.js

**Subtarefas**:
- [X] 6.4.1: Adicionar Chart.js ao projeto
- [X] 6.4.2: Criar gráfico de pizza para categorias no dashboard
- [X] 6.4.3: Criar gráfico de linha para evolução mensal
- [X] 6.4.4: Estilizar gráficos com tema escuro
- [X] 6.4.5: Adicionar responsividade aos gráficos

#### Tarefa 6.5: Otimizações de Consultas ✅
**Descrição**: Otimizar queries do banco de dados

**Subtarefas**:
- [X] 6.5.1: Adicionar select_related em queries com ForeignKey
- [X] 6.5.2: Adicionar prefetch_related onde necessário
- [X] 6.5.3: Revisar N+1 queries nos templates
- [X] 6.5.4: Adicionar índices no banco (já configurado nos models)
- [X] 6.5.5: Testar performance com dados de exemplo

#### Tarefa 6.6: Tratamento de Erros 404 e 500
**Descrição**: Criar páginas de erro personalizadas

**Subtarefas**:
- [X] 6.6.1: Criar template `templates/404.html`
- [X] 6.6.2: Estilizar página 404
- [X] 6.6.3: Adicionar link para voltar ao dashboard
- [X] 6.6.4: Criar template `templates/500.html`
- [X] 6.6.5: Estilizar página 500
- [X] 6.6.6: Configurar DEBUG = False para testar
- [X] 6.6.7: Testar páginas de erro

#### Tarefa 6.7: Documentação do Código ✅
**Descrição**: Adicionar docstrings e comentários

**Subtarefas**:
- [X] 6.7.1: Adicionar docstrings em todas as classes
- [X] 6.7.2: Adicionar docstrings em métodos complexos
- [X] 6.7.3: Comentar lógica não-óbvia
- [X] 6.7.4: Atualizar README.md com instruções de setup
- [X] 6.7.5: Documentar variáveis de ambiente necessárias

#### Tarefa 6.8: Revisão de Código ✅
**Descrição**: Revisar código seguindo boas práticas

**Subtarefas**:
- [X] 6.8.1: Verificar conformidade com PEP 8
- [X] 6.8.2: Executar linter (flake8 ou pylint)
- [X] 6.8.3: Corrigir warnings
- [X] 6.8.4: Verificar uso consistente de aspas simples
- [X] 6.8.5: Remover código comentado não utilizado
- [X] 6.8.6: Verificar imports não utilizados
- [X] 6.8.7: Organizar imports (isort)

#### Tarefa 6.9: Segurança ✅
**Descrição**: Implementar melhorias de segurança

**Subtarefas**:
- [X] 6.9.1: Configurar SECURE_SSL_REDIRECT para produção
- [X] 6.9.2: Configurar SESSION_COOKIE_SECURE
- [X] 6.9.3: Configurar CSRF_COOKIE_SECURE
- [X] 6.9.4: Adicionar SECURE_HSTS_SECONDS
- [X] 6.9.5: Revisar permissões de acesso em todas as views
- [X] 6.9.6: Testar injeção SQL (Django já protege)
- [X] 6.9.7: Testar XSS (Django já protege)

#### Tarefa 6.10: Testes Finais
**Descrição**: Realizar bateria final de testes

**Subtarefas**:
- [X] 6.10.1: Testar em Chrome
- [X] 6.10.2: Testar em Firefox
- [X] 6.10.3: Testar em Safari
- [X] 6.10.4: Testar em Edge
- [X] 6.10.5: Testar em mobile (Chrome mobile)
- [X] 6.10.6: Testar em mobile (Safari iOS)
- [X] 6.10.7: Testar com múltiplos usuários simultâneos
- [X] 6.10.8: Testar com grande volume de dados
- [X] 6.10.9: Verificar todos os fluxos críticos
- [X] 6.10.10: Listar bugs encontrados

---

### Sprint 7: Preparação para Produção (Opcional)

#### Tarefa 7.1: Configuração de Ambientes
**Descrição**: Separar configurações de desenvolvimento e produção

**Subtarefas**:
- [X] 7.1.1: Criar settings/base.py
- [X] 7.1.2: Criar settings/development.py
- [X] 7.1.3: Criar settings/production.py
- [X] 7.1.4: Configurar variáveis de ambiente
- [X] 7.1.5: Atualizar manage.py

#### Tarefa 7.2: Configuração de Arquivos Estáticos
**Descrição**: Configurar coleta de arquivos estáticos

**Subtarefas**:
- [X] 7.2.1: Configurar STATIC_ROOT
- [X] 7.2.2: Executar collectstatic
- [X] 7.2.3: Testar servindo arquivos estáticos
- [X] 7.2.4: Configurar whitenoise (opcional)

#### Tarefa 7.3: Requirements de Produção
**Descrição**: Criar arquivo de dependências para produção

**Subtarefas**:
- [X] 7.3.1: Criar requirements/base.txt
- [X] 7.3.2: Criar requirements/development.txt
- [X] 7.3.3: Criar requirements/production.txt
- [X] 7.3.4: Adicionar gunicorn ao production.txt
- [X] 7.3.5: Adicionar psycopg2 para PostgreSQL (se migrar)

#### Tarefa 7.4: Preparação de Deploy
**Descrição**: Preparar aplicação para deploy

**Subtarefas**:
- [X] 7.4.1: Criar Procfile (para Heroku, Railway, etc)
- [X] 7.4.2: Configurar allowed hosts
- [X] 7.4.3: Configurar banco de dados de produção (se aplicável)
- [X] 7.4.4: Testar com gunicorn localmente
- [X] 7.4.5: Criar checklist de deploy

---

### Sprint 8: Agente de IA Financeiro

#### Visão Geral da Sprint
Implementar funcionalidade de análise financeira personalizada usando Inteligência Artificial. O agente utilizará LangChain 1.0 integrado com OpenAI (modelo gpt-4o-mini) para analisar transações, receitas e despesas do usuário, gerando insights e recomendações personalizadas.

**Objetivo**: Adicionar capacidade de análise inteligente ao sistema, fornecendo valor adicional aos usuários através de insights automatizados sobre seus hábitos financeiros.

**Dependências**:
- Sprints 1-6 concluídas (models de User, Account, Category, Transaction)
- Dashboard funcional (Sprint 5)
- LangChain 1.0 e OpenAI API

**Entregáveis**:
- Model AIAnalysis para armazenar análises
- LangChain Tools para acesso ao banco de dados
- Agente de IA configurado e funcional
- Django Command para executar análises
- Exibição da última análise no dashboard
- Documentação técnica completa

---

#### Tarefa 8.1: Instalação de Dependências de IA
**Descrição**: Instalar e configurar LangChain e OpenAI

**Subtarefas**:
- [X] 8.1.1: Adicionar dependências ao requirements.txt:
- [X] 8.1.2: Executar `pip install -r requirements.txt`
- [X] 8.1.3: Adicionar variáveis de ambiente ao .env:
  ```
  OPENAI_API_KEY=sk-xxx
  AI_MODEL=gpt-4o-mini
  AI_MAX_TOKENS=1000
  AI_TEMPERATURE=0.7
  ```
- [X] 8.1.4: Atualizar .env.example com novas variáveis (sem valores)
- [X] 8.1.5: Configurar settings.py para ler variáveis de IA
- [X] 8.1.6: Testar import de langchain e openai no shell Django
- [X] 8.1.7: Verificar que app 'ai' está em INSTALLED_APPS
- [X] Tarefa 8.1 concluída

#### Tarefa 8.2: Model AIAnalysis
**Descrição**: Criar model Django para armazenar análises geradas pela IA

**Subtarefas**:
- [X] 8.2.1: Abrir arquivo `ai/models.py`
- [X] 8.2.2: Importar models e get_user_model
- [X] 8.2.3: Criar classe AIAnalysis
- [X] 8.2.4: Adicionar ForeignKey para User (on_delete=CASCADE)
- [X] 8.2.5: Adicionar campo analysis_text (TextField)
- [X] 8.2.6: Adicionar campo key_insights (JSONField, default=list)
- [X] 8.2.7: Adicionar campo recommendations (JSONField, default=list)
- [X] 8.2.8: Adicionar campo period_analyzed (CharField, max_length=100)
- [X] 8.2.9: Adicionar campos created_at e updated_at
- [X] 8.2.10: Adicionar método __str__ retornando user email e data
- [X] 8.2.11: Adicionar Meta com ordering por -created_at
- [X] 8.2.12: Adicionar indexes em user e created_at
- [X] 8.2.13: Adicionar verbose_name e verbose_name_plural
- [X] Tarefa 8.2 concluída

#### Tarefa 8.3: Admin de AIAnalysis
**Descrição**: Configurar Django Admin para visualizar análises

**Subtarefas**:
- [X] 8.3.1: Abrir arquivo `ai/admin.py`
- [X] 8.3.2: Importar admin e AIAnalysis
- [X] 8.3.3: Criar AIAnalysisAdmin
- [X] 8.3.4: Configurar list_display: user, period_analyzed, created_at
- [X] 8.3.5: Configurar list_filter: created_at
- [X] 8.3.6: Configurar search_fields: user__email, analysis_text
- [X] 8.3.7: Configurar readonly_fields: created_at, updated_at
- [X] 8.3.8: Configurar date_hierarchy: created_at
- [X] 8.3.9: Registrar AIAnalysis com AIAnalysisAdmin
- [X] 8.3.10: Adicionar método para exibir preview da análise
- [X] Tarefa 8.3 concluída

#### Tarefa 8.4: Migration de AIAnalysis
**Descrição**: Criar e aplicar migration

**Subtarefas**:
- [X] 8.4.1: Executar `python manage.py makemigrations ai`
- [X] 8.4.2: Revisar arquivo de migration gerado
- [X] 8.4.3: Executar `python manage.py migrate`
- [X] 8.4.4: Verificar tabela no banco de dados
- [X] 8.4.5: Testar criação manual de AIAnalysis no Django shell
- [X] Tarefa 8.4 concluída

#### Tarefa 8.5: Estrutura de Diretórios da App AI
**Descrição**: Criar estrutura de pastas e arquivos da app

**Subtarefas**:
- [X] 8.5.1: Criar diretório `ai/agents/`
- [X] 8.5.2: Criar arquivo `ai/agents/__init__.py`
- [X] 8.5.3: Criar diretório `ai/tools/`
- [X] 8.5.4: Criar arquivo `ai/tools/__init__.py`
- [X] 8.5.5: Criar diretório `ai/services/`
- [X] 8.5.6: Criar arquivo `ai/services/__init__.py`
- [X] 8.5.7: Criar diretório `ai/management/`
- [X] 8.5.8: Criar diretório `ai/management/commands/`
- [X] 8.5.9: Criar arquivo `ai/management/__init__.py`
- [X] 8.5.10: Criar arquivo `ai/management/commands/__init__.py`
- [X] Tarefa 8.5 concluída

#### Tarefa 8.6: LangChain Database Tools
**Descrição**: Criar tools LangChain para acessar dados Django

**Subtarefas**:
- [X] 8.6.1: Criar arquivo `ai/tools/database_tools.py`
- [X] 8.6.2: Importar tool decorator do LangChain
- [X] 8.6.3: Importar models: Account, Category, Transaction
- [X] 8.6.4: Criar @tool get_user_transactions
  - Parâmetro: user_id (int)
  - Retorna: lista de transações dos últimos 30 dias
  - Formato: dict com data, valor, tipo, categoria, descrição
- [X] 8.6.5: Criar @tool get_user_accounts
  - Parâmetro: user_id (int)
  - Retorna: lista de contas com nome, banco, saldo
- [X] 8.6.6: Criar @tool get_user_categories
  - Parâmetro: user_id (int)
  - Retorna: categorias com nome e tipo
- [X] 8.6.7: Criar @tool get_spending_by_category
  - Parâmetro: user_id (int)
  - Retorna: total gasto por categoria (últimos 30 dias)
  - Ordenado do maior para o menor
- [X] 8.6.8: Criar @tool get_income_vs_expense
  - Parâmetro: user_id (int)
  - Retorna: total receitas, total despesas, saldo
  - Período: últimos 30 dias
- [X] 8.6.9: Adicionar docstrings detalhadas em cada tool
- [X] 8.6.10: Adicionar tratamento de exceções
- [X] 8.6.11: Testar tools individualmente no shell
- [X] Tarefa 8.6 concluída

#### Tarefa 8.7: Agente LangChain de Finanças
**Descrição**: Implementar agente de IA usando LangChain

**Subtarefas**:
- [X] 8.7.1: Criar arquivo `ai/agents/finance_insight_agent.py`
- [X] 8.7.2: Importar ChatOpenAI do langchain-openai
- [X] 8.7.3: Importar create_tool_calling_agent, AgentExecutor (v1.0: create_agent)
- [X] 8.7.4: Importar ChatPromptTemplate
- [X] 8.7.5: Importar tools de database_tools
- [X] 8.7.6: Criar função initialize_agent(user_id: int)
- [X] 8.7.7: Configurar ChatOpenAI com variáveis de ambiente
- [X] 8.7.8: Definir system prompt detalhado:
  ```
  Você é um assistente financeiro pessoal especializado em análise de gastos.
  Analise os dados do usuário e forneça:
  1. Visão geral clara e objetiva
  2. 3-5 insights principais sobre padrões de gasto
  3. 3-5 recomendações práticas e acionáveis
  4. Tom amigável e motivador em português
  Use emojis para tornar a leitura mais agradável.
  ```
- [X] 8.7.9: Criar prompt template com system e user messages
- [X] 8.7.10: Criar agente com create_tool_calling_agent (v1.0: create_agent)
- [X] 8.7.11: Criar AgentExecutor com agente e tools (v1.0: CompiledStateGraph)
- [X] 8.7.12: Criar função run_analysis(user_id: int) -> dict
- [X] 8.7.13: Função deve retornar dict com analysis_text, insights, recommendations
- [X] 8.7.14: Adicionar logging de execução
- [X] 8.7.15: Adicionar tratamento de erros OpenAI
- [X] 8.7.16: Testar agente manualmente no shell
- [X] Tarefa 8.7 concluída

#### Tarefa 8.8: Serviço de Análise
**Descrição**: Criar camada de serviço para orquestrar análise

**Subtarefas**:
- [X] 8.8.1: Criar arquivo `ai/services/analysis_service.py`
- [X] 8.8.2: Importar AIAnalysis model
- [X] 8.8.3: Importar get_user_model
- [X] 8.8.4: Importar funções do finance_insight_agent
- [X] 8.8.5: Criar função generate_analysis_for_user(user_id: int)
- [X] 8.8.6: Validar que usuário existe
- [X] 8.8.7: Verificar última análise (não gerar se < 24h)
- [X] 8.8.8: Chamar run_analysis do agente
- [X] 8.8.9: Parsear resultado do agente
- [X] 8.8.10: Extrair insights e recommendations do texto
- [X] 8.8.11: Criar objeto AIAnalysis e salvar no banco
- [X] 8.8.12: Retornar AIAnalysis criado
- [X] 8.8.13: Adicionar logging detalhado
- [X] 8.8.14: Adicionar tratamento de exceções completo
- [X] 8.8.15: Adicionar função get_latest_analysis(user_id: int)
- [X] Tarefa 8.8 concluída

#### Tarefa 8.9: Django Command
**Descrição**: Criar comando para executar análise via CLI

**Subtarefas**:
- [X] 8.9.1: Criar arquivo `ai/management/commands/run_finance_analysis.py`
- [X] 8.9.2: Importar BaseCommand
- [X] 8.9.3: Importar get_user_model
- [X] 8.9.4: Importar generate_analysis_for_user
- [X] 8.9.5: Criar classe Command(BaseCommand)
- [X] 8.9.6: Definir help text descritivo
- [X] 8.9.7: Adicionar argumento --user-email (opcional)
- [X] 8.9.8: Adicionar flag --all para todos os usuários
- [X] 8.9.9: Implementar handle method
- [X] 8.9.10: Se --user-email: processar apenas esse usuário
- [X] 8.9.11: Se --all: iterar sobre todos os usuários ativos
- [X] 8.9.12: Adicionar output informativo (self.stdout.write)
- [X] 8.9.13: Adicionar barra de progresso para --all (opcional)
- [X] 8.9.14: Adicionar tratamento de erros por usuário
- [X] 8.9.15: Testar comando: `python manage.py run_finance_analysis --user-email test@test.com`
- [X] Tarefa 8.9 concluída

#### Tarefa 8.10: Exibição no Dashboard
**Descrição**: Mostrar última análise no dashboard do usuário

**Subtarefas**:
- [X] 8.10.1: Abrir `users/views.py` (ou app do dashboard)
- [X] 8.10.2: Importar AIAnalysis model
- [X] 8.10.3: No get_context_data do DashboardView:
- [X] 8.10.4: Buscar última análise do usuário:
  ```python
  latest_analysis = AIAnalysis.objects.filter(
      user=self.request.user
  ).order_by('-created_at').first()
  ```
- [X] 8.10.5: Adicionar latest_analysis ao context
- [X] 8.10.6: Abrir template `templates/dashboard.html`
- [X] 8.10.7: Criar seção "Análise Financeira IA" após estatísticas
- [X] 8.10.8: Verificar {% if latest_analysis %}
- [X] 8.10.9: Exibir card com gradiente destacado
- [X] 8.10.10: Exibir ícone de IA (🤖)
- [X] 8.10.11: Exibir título "Sua Análise Financeira Personalizada"
- [X] 8.10.12: Exibir data da análise (created_at)
- [X] 8.10.13: Exibir analysis_text formatado (preservar quebras de linha)
- [X] 8.10.14: Adicionar botão "Gerar Nova Análise" (futuro)
- [X] 8.10.15: Se não houver análise, mostrar call-to-action
- [X] 8.10.16: Estilizar com TailwindCSS seguindo design system
- [X] Tarefa 8.10 concluída

#### Tarefa 8.11: Template da Análise
**Descrição**: Criar componente visual para exibir análise

**Subtarefas**:
- [ ] 8.11.1: Criar parcial `templates/includes/ai_analysis_card.html`
- [ ] 8.11.2: Receber analysis como parâmetro
- [ ] 8.11.3: Criar card com bg-gradient (roxo/azul)
- [ ] 8.11.4: Header com ícone 🤖 e título
- [ ] 8.11.5: Data de geração em formato legível
- [ ] 8.11.6: Corpo com analysis_text formatado
- [ ] 8.11.7: Usar white-space: pre-wrap para manter formatação
- [ ] 8.11.8: Seção de insights destacada (se existir)
- [ ] 8.11.9: Seção de recomendações destacada (se existir)
- [ ] 8.11.10: Footer com link "Ver análises anteriores" (futuro)
- [ ] 8.11.11: Responsividade mobile
- [ ] 8.11.12: Incluir no dashboard.html: {% include 'includes/ai_analysis_card.html' %}

#### Tarefa 8.12: Testes Manuais da IA
**Descrição**: Testar funcionalidade completa

**Subtarefas**:
- [ ] 8.12.1: Criar usuário de teste com dados financeiros variados
- [ ] 8.12.2: Adicionar 5-10 contas bancárias
- [ ] 8.12.3: Adicionar 20-30 transações de tipos diferentes
- [ ] 8.12.4: Executar comando: `python manage.py run_finance_analysis --user-email test@example.com`
- [ ] 8.12.5: Verificar que análise foi gerada no terminal
- [ ] 8.12.6: Verificar que AIAnalysis foi criado no banco (admin)
- [ ] 8.12.7: Acessar dashboard e verificar exibição da análise
- [ ] 8.12.8: Verificar formatação e estilo da análise
- [ ] 8.12.9: Tentar gerar nova análise antes de 24h (deve bloquear)
- [ ] 8.12.10: Testar com usuário sem transações (deve lidar graciosamente)
- [ ] 8.12.11: Testar comando --all com múltiplos usuários
- [ ] 8.12.12: Verificar logs de execução

#### Tarefa 8.13: Documentação Técnica AI
**Descrição**: Criar documentação sobre o sistema de IA

**Subtarefas**:
- [ ] 8.13.1: Criar arquivo `docs/ai-financial-agent.md`
- [ ] 8.13.2: Seção: Visão Geral da Funcionalidade
- [ ] 8.13.3: Seção: Arquitetura e Fluxo de Dados
- [ ] 8.13.4: Seção: LangChain Tools Disponíveis
- [ ] 8.13.5: Seção: Configuração (variáveis de ambiente)
- [ ] 8.13.6: Seção: Como Executar Análises (comando Django)
- [ ] 8.13.7: Seção: Estrutura do Prompt do Agente
- [ ] 8.13.8: Seção: Formato de Saída da Análise
- [ ] 8.13.9: Seção: Segurança e Isolamento de Dados
- [ ] 8.13.10: Seção: Limitações e Expansões Futuras
- [ ] 8.13.11: Seção: Troubleshooting
- [ ] 8.13.12: Adicionar exemplos de uso
- [ ] 8.13.13: Adicionar link no docs/README.md

#### Tarefa 8.14: Agente Especialista em IA
**Descrição**: Criar documento de referência para integração de IA

**Subtarefas**:
- [ ] 8.14.1: Criar arquivo `ai/agents/ai_integration_expert.md`
- [ ] 8.14.2: Seção: Visão Geral do Papel
- [ ] 8.14.3: Seção: LangChain 1.0 - Conceitos Fundamentais
- [ ] 8.14.4: Seção: Padrões de Integração com Django
- [ ] 8.14.5: Seção: Como Criar Tools para Acesso a Dados
- [ ] 8.14.6: Seção: Design de Prompts Eficazes
- [ ] 8.14.7: Seção: Configuração de Agentes (AgentExecutor)
- [ ] 8.14.8: Seção: Tratamento de Erros e Logging
- [ ] 8.14.9: Seção: Uso do MCP Context7 para Docs LangChain
- [ ] 8.14.10: Seção: Boas Práticas de Segurança
- [ ] 8.14.11: Seção: Testes e Validação de Agentes
- [ ] 8.14.12: Incluir exemplos de código completos
- [ ] 8.14.13: Incluir fluxo de desenvolvimento passo a passo

#### Tarefa 8.15: Atualização de Documentação Geral
**Descrição**: Atualizar documentos do projeto

**Subtarefas**:
- [ ] 8.15.1: Atualizar README.md com seção sobre IA
- [ ] 8.15.2: Adicionar instruções de configuração da API OpenAI
- [ ] 8.15.3: Adicionar comando run_finance_analysis ao README
- [ ] 8.15.4: Atualizar CLAUDE.md com padrões de código para AI app
- [ ] 8.15.5: Atualizar docs/architecture.md incluindo AI app
- [ ] 8.15.6: Atualizar docs/data-models.md com AIAnalysis
- [ ] 8.15.7: Criar diagrama ER incluindo AIAnalysis
- [ ] 8.15.8: Atualizar agents/README.md com ai_integration_expert

#### Tarefa 8.16: Refinamentos e Otimizações
**Descrição**: Melhorias finais e polish

**Subtarefas**:
- [ ] 8.16.1: Adicionar rate limiting no serviço (1 análise/24h)
- [ ] 8.16.2: Implementar cache de análises recentes
- [ ] 8.16.3: Adicionar métricas de uso (tempo de execução, tokens usados)
- [ ] 8.16.4: Melhorar parsing de insights/recommendations
- [ ] 8.16.5: Adicionar fallback se API OpenAI falhar
- [ ] 8.16.6: Melhorar mensagens de erro para usuário
- [ ] 8.16.7: Adicionar logging estruturado
- [ ] 8.16.8: Otimizar queries das tools (select_related)
- [ ] 8.16.9: Adicionar validação de dados antes de enviar ao LLM
- [ ] 8.16.10: Testar com dados edge case (0 transações, etc)

#### Tarefa 8.17: Segurança e Compliance
**Descrição**: Validar aspectos de segurança

**Subtarefas**:
- [ ] 8.17.1: Verificar que API key não está em código
- [ ] 8.17.2: Verificar isolamento de dados por usuário em todas as tools
- [ ] 8.17.3: Adicionar validação de user_id em tools
- [ ] 8.17.4: Testar que usuário A não vê dados de usuário B
- [ ] 8.17.5: Verificar que prompts não vazam dados sensíveis
- [ ] 8.17.6: Adicionar rate limiting por usuário
- [ ] 8.17.7: Verificar que logs não expõem dados financeiros
- [ ] 8.17.8: Documentar política de privacidade para IA
- [ ] 8.17.9: Adicionar disclaimer sobre uso de IA
- [ ] 8.17.10: Testar LGPD compliance (direito ao esquecimento)

---

### Sprint 9: Testes Automatizados

#### Tarefa 9.1: Configuração de Testes
**Descrição**: Configurar ambiente de testes

**Subtarefas**:
- [ ] 9.1.1: Criar diretório tests em cada app
- [ ] 9.1.2: Configurar pytest-django (opcional)
- [ ] 9.1.3: Criar factories com factory_boy (opcional)
- [ ] 9.1.4: Configurar coverage

#### Tarefa 9.2: Testes de Models
**Descrição**: Criar testes para models

**Subtarefas**:
- [ ] 9.2.1: Testes de CustomUser
- [ ] 9.2.2: Testes de Profile
- [ ] 9.2.3: Testes de Account
- [ ] 9.2.4: Testes de Category
- [ ] 9.2.5: Testes de Transaction
- [ ] 9.2.6: Testar métodos __str__
- [ ] 9.2.7: Testar validações

#### Tarefa 9.3: Testes de Views
**Descrição**: Criar testes para views

**Subtarefas**:
- [ ] 9.3.1: Testes de autenticação (signup, login, logout)
- [ ] 9.3.2: Testes de CRUD de contas
- [ ] 9.3.3: Testes de CRUD de categorias
- [ ] 9.3.4: Testes de CRUD de transações
- [ ] 9.3.5: Testes de dashboard
- [ ] 9.3.6: Testes de perfil
- [ ] 9.3.7: Testar permissões de acesso

#### Tarefa 9.4: Testes de Signals
**Descrição**: Testar signals e lógica de negócio

**Subtarefas**:
- [ ] 9.4.1: Testar criação automática de perfil
- [ ] 9.4.2: Testar criação de categorias padrão
- [ ] 9.4.3: Testar atualização de saldo ao criar transação
- [ ] 9.4.4: Testar atualização de saldo ao editar transação
- [ ] 9.4.5: Testar atualização de saldo ao excluir transação

#### Tarefa 9.5: Testes de Integração
**Descrição**: Testar fluxos completos

**Subtarefas**:
- [ ] 9.5.1: Testar fluxo completo de cadastro e primeira transação
- [ ] 9.5.2: Testar fluxo de múltiplas transações e saldo
- [ ] 9.5.3: Testar fluxo de filtros e busca
- [ ] 9.5.4: Testar isolamento entre usuários

#### Tarefa 9.6: Executar e Analisar Coverage
**Descrição**: Verificar cobertura de testes

**Subtarefas**:
- [ ] 9.6.1: Executar todos os testes
- [ ] 9.6.2: Gerar relatório de coverage
- [ ] 9.6.3: Identificar áreas sem cobertura
- [ ] 9.6.4: Adicionar testes faltantes
- [ ] 9.6.5: Atingir pelo menos 80% de cobertura

---

### Sprint 10: Docker e CI/CD (Sprint Final)

#### Tarefa 10.1: Dockerfile
**Descrição**: Criar Dockerfile para containerização

**Subtarefas**:
- [ ] 10.1.1: Criar Dockerfile na raiz do projeto
- [ ] 10.1.2: Usar imagem Python oficial
- [ ] 10.1.3: Configurar workdir
- [ ] 10.1.4: Copiar requirements e instalar
- [ ] 10.1.5: Copiar código da aplicação
- [ ] 10.1.6: Configurar comando de inicialização
- [ ] 10.1.7: Testar build da imagem

#### Tarefa 10.2: Docker Compose
**Descrição**: Criar docker-compose para ambiente completo

**Subtarefas**:
- [ ] 10.2.1: Criar docker-compose.yml
- [ ] 10.2.2: Configurar serviço web
- [ ] 10.2.3: Configurar serviço de banco (PostgreSQL se migrar)
- [ ] 10.2.4: Configurar volumes
- [ ] 10.2.5: Configurar networks
- [ ] 10.2.6: Testar com docker-compose up

#### Tarefa 10.3: CI/CD com GitHub Actions
**Descrição**: Configurar pipeline de CI/CD

**Subtarefas**:
- [ ] 10.3.1: Criar .github/workflows/ci.yml
- [ ] 10.3.2: Configurar job de testes
- [ ] 10.3.3: Configurar job de linting
- [ ] 10.3.4: Configurar job de build
- [ ] 10.3.5: Configurar deploy automático (opcional)
- [ ] 10.3.6: Testar pipeline

#### Tarefa 10.4: Documentação Final
**Descrição**: Finalizar documentação do projeto

**Subtarefas**:
- [ ] 10.4.1: Atualizar docs/README.md completo
- [ ] 10.4.2: Documentar variáveis de ambiente
- [ ] 10.4.3: Documentar comandos úteis
- [ ] 10.4.4: Criar guia de contribuição (se open source)
- [ ] 10.4.5: Documentar processo de deploy
- [ ] 10.4.6: Criar CHANGELOG.md
