# Finanpy - Financial Management System

## Project Overview

Finanpy is a personal finance management system built with Python and Django. It's designed to provide users with a simple, efficient, and accessible tool to organize their personal finances, track income and expenses, categorize transactions, and make more conscious financial decisions through clear visualizations. The application features a modern, dark-themed UI with TailwindCSS and follows a full-stack approach using Django Template Language.

### Key Features
- User authentication with email-based login
- Personal finance dashboard with financial overview
- Bank account management
- Transaction categorization system
- Income and expense tracking
- Financial reporting and visualizations
- Multi-account support
- Responsive design for desktop, tablet, and mobile

### Tech Stack
- **Backend**: Python 3.13+, Django 5+
- **Database**: SQLite3 (default), PostgreSQL ready
- **Frontend**: Django Template Language + TailwindCSS
- **Authentication**: Django Auth (custom email-based)
- **CSS Framework**: TailwindCSS with custom dark theme
- **Development Server**: Django Development Server

## Project Structure

```
finanpy/
├── accounts/           # Bank account management module
├── agents/             # AI agent functionality
├── ai_summary_reports/ # AI-generated financial reports
├── categories/         # Transaction categories module
├── core/              # Main project settings and URLs
├── docs/              # Documentation
├── profiles/          # User profile management
├── static/            # CSS, JavaScript, and image assets
├── templates/         # Django HTML templates
├── theme/             # TailwindCSS configuration
├── transactions/      # Transaction management module
├── users/             # User authentication and management
├── .env.example       # Environment configuration template
├── .flake8            # Flake8 configuration
├── .isort.cfg         # Import sorting configuration
├── manage.py          # Django management utility
├── requirements.txt   # Python dependencies
└── other config files
```

## Building and Running

### Prerequisites
- Python 3.13+
- pip package manager
- Virtual environment (recommended)

### Setup Instructions

1. **Clone and setup virtual environment:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables:**
```bash
cp .env.example .env
```
Generate a secret key and update your `.env` file:
```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

4. **Run database migrations:**
```bash
python manage.py makemigrations
python manage.py migrate
```

5. **Create a superuser (optional):**
```bash
python manage.py createsuperuser
```

6. **Compile TailwindCSS (if needed):**
```bash
python manage.py tailwind install
python manage.py tailwind build
```

7. **Run the development server:**
```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

### Development Commands

- **Run tests:** `python manage.py test`
- **Start Tailwind watch:** `python manage.py tailwind start`
- **Check code style:** `flake8 .`
- **Format imports:** `isort .`

## Main Django Apps

### 1. `users/` App
- Custom User model using email instead of username
- Authentication views (login, signup, logout)
- Dashboard view with financial statistics

### 2. `profiles/` App
- User profile management
- Additional user information beyond authentication

### 3. `accounts/` App
- Bank account management
- Creation, editing, deletion of accounts
- Balance tracking

### 4. `categories/` App
- Transaction categorization system
- Support for income and expense categories
- Color-coded categories for visual distinction

### 5. `transactions/` App
- Income and expense tracking
- Transaction management with date, amount, description
- Linking to accounts and categories

## Development Conventions

### Code Style
- Follow PEP 8 Python coding standards
- Use single quotes for strings
- Code should be written in English
- All models should have `created_at` and `updated_at` fields

### Security
- Passwords stored with Django's secure hashing
- Protected routes using LoginRequiredMixin
- User data isolated per user account
- HTTPS recommended for production

### Frontend
- TailwindCSS for styling
- Responsive design supporting mobile, tablet, desktop
- Dark theme with primary gradient colors
- Accessible UI components

## Database Schema

The application uses a well-structured database with the following main models:

- **CustomUser**: Email-based authentication
- **Profile**: Extended user information
- **Account**: Bank account information with balances
- **Category**: Transaction categories for income/expense
- **Transaction**: Financial transactions linked to accounts and categories

## Environment Variables

The project uses environment configuration via `.env` file:

- `SECRET_KEY`: Django secret key for cryptographic operations
- `DEBUG`: Debug mode flag (True for development, False for production)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hostnames
- Security settings for production HTTPS deployment

## Deployment Notes

For production deployment:
- Set `DEBUG=False`
- Use PostgreSQL instead of SQLite
- Configure proper ALLOWED_HOSTS
- Enable all security settings (HTTPS, HSTS, etc.)
- Use a proper WSGI server like Gunicorn
- Configure reverse proxy with Nginx

## Testing

The application follows Django's testing framework with tests written for each app. Tests should cover:
- Functional requirements (authentication, CRUD operations)
- Business logic (financial calculations)
- Security (user data isolation)
- Performance (response times)

## Known Limitations

- SQLite database has limitations with concurrent users
- TailwindCSS compilation required for styling changes
- Currently in development phase (MVP)