# Arquitetura do Projeto

## Estrutura de Diretórios

```
finanpy/
├── core/              # Configurações globais e URLs principais
├── users/             # Extensão do User model do Django
├── profiles/          # Perfis de usuários
├── accounts/          # Contas bancárias
├── categories/        # Categorias de transações
├── transactions/      # Transações financeiras
├── docs/              # Documentação do projeto
├── manage.py          # Script de gerenciamento Django
├── requirements.txt   # Dependências do projeto
├── db.sqlite3         # Banco de dados SQLite
└── PRD.md            # Product Requirements Document
```

## Apps Django

O projeto está organizado em apps Django com responsabilidades bem definidas:

### core/
Configurações centrais do projeto Django.

**Responsabilidades**:
- Configurações globais (`settings.py`)
- URLs principais (`urls.py`)
- WSGI e ASGI configuration

**Arquivos principais**:
- `settings.py`: Configurações do Django, apps instalados, middleware, database
- `urls.py`: Roteamento principal de URLs
- `wsgi.py`: Interface WSGI para deploy
- `asgi.py`: Interface ASGI para aplicações assíncronas

### users/
Gerenciamento de usuários do sistema.

**Responsabilidades**:
- Autenticação de usuários
- Cadastro e login
- Extensão do modelo User padrão do Django

**Models**: Usa o User model padrão do Django (`django.contrib.auth`)

### profiles/
Perfis complementares aos usuários.

**Responsabilidades**:
- Informações adicionais do usuário (nome completo, telefone)
- Relação one-to-one com User
- Criação automática de perfil ao cadastrar usuário

**Fields esperados**:
- `user`: ForeignKey para User (OneToOne)
- `full_name`: Nome completo do usuário
- `phone`: Telefone de contato
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### accounts/
Gerenciamento de contas bancárias.

**Responsabilidades**:
- CRUD de contas bancárias
- Controle de saldo de cada conta
- Associação de contas ao usuário

**Fields esperados**:
- `user`: ForeignKey para User
- `name`: Nome da conta
- `bank_name`: Nome do banco
- `account_type`: Tipo de conta (corrente, poupança, etc.)
- `balance`: Saldo atual
- `is_active`: Status da conta
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### categories/
Categorização de transações.

**Responsabilidades**:
- CRUD de categorias
- Diferenciação entre categorias de entrada e saída
- Personalização por usuário

**Fields esperados**:
- `user`: ForeignKey para User
- `name`: Nome da categoria
- `category_type`: Tipo (income/expense)
- `color`: Cor para identificação visual
- `created_at`: Data de criação
- `updated_at`: Data de atualização

### transactions/
Registro de transações financeiras.

**Responsabilidades**:
- CRUD de transações
- Associação com contas e categorias
- Registro de entradas e saídas
- Filtragem por período, conta e categoria

**Fields esperados**:
- `account`: ForeignKey para Account
- `category`: ForeignKey para Category
- `transaction_type`: Tipo (income/expense)
- `amount`: Valor da transação
- `transaction_date`: Data da transação
- `description`: Descrição/observação
- `created_at`: Data de criação
- `updated_at`: Data de atualização

## Arquitetura de Dados

### Relacionamentos

```
User (Django Auth)
  ↓ OneToOne
Profile

User
  ↓ OneToMany
Account
  ↓ OneToMany
Transaction
  ↓ ManyToOne
Category
  ↓ ManyToOne
User
```

### Fluxo de Dados

1. **Usuário** se cadastra no sistema
2. **Profile** é criado automaticamente
3. Usuário cria **Accounts** (contas bancárias)
4. Usuário cria **Categories** para organização
5. Usuário registra **Transactions** associadas a contas e categorias
6. Sistema calcula saldos e apresenta no dashboard

## Padrões Arquiteturais

### MTV (Model-Template-View)
O projeto segue o padrão MTV do Django:
- **Models**: Definição de dados e lógica de negócio
- **Templates**: Apresentação visual (Django Template Language)
- **Views**: Lógica de controle e processamento

### Apps Modulares
Cada funcionalidade está isolada em seu próprio app, facilitando:
- Manutenção independente
- Reuso de código
- Testes isolados
- Escalabilidade

### Convenções de Código
- Código em inglês
- Aspas simples
- PEP 8
- Todos os models têm `created_at` e `updated_at`

## Banco de Dados

### SQLite3
- Banco de dados padrão do Django
- Ideal para desenvolvimento e MVP
- Arquivo único: `db.sqlite3`

### Migração Futura
A arquitetura permite migração fácil para PostgreSQL quando necessário, sem alteração de código dos models.

## Segurança

### Autenticação
- Django Auth nativo
- Hash de senhas com PBKDF2
- Validação de força de senha

### Proteção de Rotas
- Middleware de autenticação
- Decoradores `@login_required`
- Isolamento de dados por usuário

### CSRF Protection
- Middleware CSRF ativo
- Tokens em todos os formulários

## Performance

### Query Optimization
- Use `select_related()` para ForeignKeys
- Use `prefetch_related()` para relações reversas
- Evite N+1 queries

### Caching
- Template fragment caching quando necessário
- Database query caching para relatórios

## Escalabilidade

O projeto está preparado para:
- Migração para PostgreSQL
- Adição de novos apps/módulos
- Implementação de API REST (Django REST Framework)
- Deploy em serviços cloud (Heroku, AWS, etc.)
