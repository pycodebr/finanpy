# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Finanpy is a personal finance management system built with Django 5+ and Python 3.13+. The system uses Django Template Language with TailwindCSS for the frontend, following a full-stack monolithic architecture focused on simplicity and avoiding over-engineering.

**Core Functionality**: Users manage bank accounts, categorize transactions (income/expense), and view consolidated financial data through a dashboard.

## Architecture

### App Structure and Responsibilities

The project follows Django's modular app pattern with strict data isolation per user:

- **core/**: Django configuration, global URLs, settings
- **users/**: Authentication using Django's native User model
- **profiles/**: User profiles (OneToOne with User), auto-created via signal
- **accounts/**: Bank accounts (belongs to User, contains Transactions)
- **categories/**: Transaction categories with type (income/expense), user-specific
- **transactions/**: Financial transactions linking Account + Category

### Data Flow and Relationships

```
User (Django Auth)
  ├── Profile (1:1, auto-created)
  ├── Account (1:N)
  │   └── Transaction (1:N)
  │       └── Category (N:1, PROTECT on delete)
  └── Category (1:N)
```

**Critical Security Pattern**: ALL data queries MUST filter by `user=request.user`. Never expose cross-user data.

### Key Architectural Decisions

1. **Profile Creation**: Automatic via `post_save` signal when User is created
2. **Category Deletion**: Uses `on_delete=PROTECT` to prevent deletion if transactions exist
3. **Account Deletion**: CASCADE - deletes all associated transactions
4. **Balance Calculation**: Derived from transaction aggregation (income - expense)

## Code Standards (Strictly Enforced)

### Python Conventions
- **Quotes**: Single quotes `'` for all strings (exception: strings containing single quotes)
- **Naming**: English only, snake_case for variables/functions, PascalCase for classes
- **PEP 8**: Follow strictly, max line 79-120 characters
- **Imports**: Grouped (stdlib, Django, local) with blank lines between

### Django Patterns

**Required in ALL models**:
```python
created_at = models.DateTimeField(auto_now_add=True)
updated_at = models.DateTimeField(auto_now=True)
```

**View Protection**:
```python
from django.contrib.auth.decorators import login_required

@login_required
def view_name(request):
    # ALWAYS filter by user
    items = Model.objects.filter(user=request.user)
```

**Query Optimization**:
- Use `select_related()` for ForeignKey relationships
- Use `prefetch_related()` for reverse ForeignKey
- Avoid N+1 queries in templates

### Template Structure
- Templates in `<app>/templates/<app>/` following Django convention
- Naming: `list.html`, `form.html`, `detail.html`, `confirm_delete.html`

## Development Commands

### Setup and Running
```bash
# Activate virtual environment
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

# Database migrations
python manage.py makemigrations
python manage.py migrate

# Run development server
python manage.py runserver

# Create admin user
python manage.py createsuperuser
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations <app_name>

# Check migration status
python manage.py showmigrations

# Interactive shell
python manage.py shell
```

### Testing
```bash
# Run all tests
python manage.py test

# Test specific app
python manage.py test <app_name>

# Keep database between test runs
python manage.py test --keepdb
```

## Design System

### Color Palette (TailwindCSS)
- **Primary Gradient**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Backgrounds**: `#0f172a` (primary), `#1e293b` (secondary), `#334155` (tertiary)
- **Text**: `#f1f5f9` (primary), `#cbd5e1` (secondary), `#64748b` (muted)
- **States**: `#10b981` (success/income), `#ef4444` (error/expense)

### Transaction Type Conventions
- **Income**: Use green colors, "+" prefix, `transaction_type='income'`
- **Expense**: Use red colors, "-" prefix, `transaction_type='expense'`
- **Validation**: Transaction type MUST match category type

## Common Patterns

### Creating a New App
1. `python manage.py startapp <app_name>`
2. Add to `INSTALLED_APPS` in `core/settings.py`
3. Create models with required `created_at` and `updated_at` fields
4. Define `__str__` method and Meta class (verbose_name, ordering)
5. Create migrations and apply
6. Register in admin if needed

### Data Isolation Example
```python
# CORRECT
accounts = Account.objects.filter(user=request.user)

# WRONG - security violation
accounts = Account.objects.all()
```

### Form Handling Pattern
```python
if request.method == 'POST':
    form = AccountForm(request.POST)
    if form.is_valid():
        account = form.save(commit=False)
        account.user = request.user  # Always set user
        account.save()
        return redirect('accounts:list')
```

## Documentation

Comprehensive documentation in `/docs/`:
- `architecture.md`: App structure and design decisions
- `coding-standards.md`: Full coding guidelines and examples
- `design-system.md`: Complete UI components and styling
- `data-models.md`: Detailed model specifications
- `setup.md`: Environment setup and workflows

Refer to `PRD.md` for complete functional requirements and user flows.

## Project Philosophy

**Avoid over-engineering**: Use Django's built-in features (auth, admin, forms) rather than custom solutions. Keep code simple, direct, and maintainable. Templates use Django Template Language (not a JavaScript framework) for server-side rendering.
