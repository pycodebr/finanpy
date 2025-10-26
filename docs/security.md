# Security Documentation - Finanpy

This document outlines the security measures implemented in the Finanpy application and provides guidance for secure deployment.

## Sprint 6 - Tarefa 6.9: Security Implementation Summary

All security subtasks have been completed and verified:

- **6.9.1**: SECURE_SSL_REDIRECT configured for production
- **6.9.2**: SESSION_COOKIE_SECURE configured for production
- **6.9.3**: CSRF_COOKIE_SECURE configured for production
- **6.9.4**: SECURE_HSTS_SECONDS configured with 1-year duration
- **6.9.5**: All views reviewed and verified for proper permissions
- **6.9.6**: SQL injection protection verified (Django ORM only)
- **6.9.7**: XSS protection verified (autoescaping enabled)

---

## 1. HTTPS and SSL Configuration (6.9.1)

### Implementation

**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (lines 154-157)

```python
if not DEBUG:
    # Force all connections to use HTTPS instead of HTTP
    SECURE_SSL_REDIRECT = config('SECURE_SSL_REDIRECT', default=True, cast=bool)
```

### Purpose
- Automatically redirects all HTTP requests to HTTPS in production
- Prevents man-in-the-middle attacks by ensuring encrypted connections
- Only active when `DEBUG=False` to allow local development

### Configuration
- **Environment Variable**: `SECURE_SSL_REDIRECT=True`
- **Default**: Automatically enabled in production (DEBUG=False)
- **Requirement**: Valid SSL/TLS certificate must be configured on your web server

### Deployment Checklist
- [ ] Obtain and install SSL certificate (Let's Encrypt, commercial CA, or cloud provider)
- [ ] Configure web server (Nginx/Apache) or load balancer for HTTPS
- [ ] Verify HTTPS is working before enabling this setting
- [ ] Test with `SECURE_SSL_REDIRECT=True` in staging environment

---

## 2. Session Cookie Security (6.9.2)

### Implementation

**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (lines 159-161)

```python
if not DEBUG:
    # Ensure session cookies are only sent over HTTPS
    SESSION_COOKIE_SECURE = config('SESSION_COOKIE_SECURE', default=True, cast=bool)
```

### Purpose
- Prevents session cookies from being transmitted over insecure HTTP connections
- Protects against session hijacking via network sniffing
- Critical for protecting user authentication state

### Security Impact
Without this setting, an attacker on the same network could:
- Intercept session cookies over HTTP
- Impersonate the user
- Gain unauthorized access to the account

### Configuration
- **Environment Variable**: `SESSION_COOKIE_SECURE=True`
- **Default**: Automatically enabled in production (DEBUG=False)
- **Requirement**: Site must be fully accessible via HTTPS

---

## 3. CSRF Cookie Security (6.9.3)

### Implementation

**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (lines 163-165)

```python
if not DEBUG:
    # Ensure CSRF cookies are only sent over HTTPS
    CSRF_COOKIE_SECURE = config('CSRF_COOKIE_SECURE', default=True, cast=bool)
```

### Purpose
- Ensures CSRF protection tokens are only transmitted over secure connections
- Prevents CSRF token theft via network sniffing
- Works in conjunction with Django's built-in CSRF middleware

### Security Impact
- Protects against Cross-Site Request Forgery attacks
- Prevents attackers from forging authenticated requests
- Essential for protecting state-changing operations (create, update, delete)

### Configuration
- **Environment Variable**: `CSRF_COOKIE_SECURE=True`
- **Default**: Automatically enabled in production (DEBUG=False)
- **Note**: Django's CSRF middleware is already enabled in MIDDLEWARE

---

## 4. HTTP Strict Transport Security - HSTS (6.9.4)

### Implementation

**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (lines 167-177)

```python
if not DEBUG:
    # HSTS Configuration
    SECURE_HSTS_SECONDS = config('SECURE_HSTS_SECONDS', default=31536000, cast=int)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = config('SECURE_HSTS_INCLUDE_SUBDOMAINS', default=True, cast=bool)
    SECURE_HSTS_PRELOAD = config('SECURE_HSTS_PRELOAD', default=True, cast=bool)
```

### Purpose
- Instructs browsers to ONLY access the site via HTTPS for the specified duration
- Prevents protocol downgrade attacks
- Protects against cookie hijacking and SSL stripping attacks

### Configuration Details

**SECURE_HSTS_SECONDS**: `31536000` (1 year)
- Duration (in seconds) that browsers will remember to only use HTTPS
- Recommended: Start with 300 seconds (5 minutes) for testing
- Production: 31536000 seconds (1 year) or longer

**SECURE_HSTS_INCLUDE_SUBDOMAINS**: `True`
- Applies HSTS policy to all subdomains
- Only enable if ALL subdomains support HTTPS
- Be cautious if you have multiple subdomains

**SECURE_HSTS_PRELOAD**: `True`
- Allows submission to browser HSTS preload lists
- Requires HSTS_SECONDS >= 1 year and INCLUDE_SUBDOMAINS=True
- See: https://hstspreload.org/

### Important Warnings

**WARNING**: HSTS is irreversible for the duration specified!
- Once enabled, browsers will refuse HTTP connections
- Cannot be disabled client-side before expiration
- Test thoroughly in staging before production

**Recommended Deployment Strategy**:
1. Start with `SECURE_HSTS_SECONDS=300` (5 minutes)
2. Test thoroughly for 24-48 hours
3. Increase to `SECURE_HSTS_SECONDS=86400` (1 day)
4. Test for another week
5. Finally set to `SECURE_HSTS_SECONDS=31536000` (1 year)

---

## 5. View Permission Review (6.9.5)

### Methodology
All view files were audited to verify:
- Proper authentication requirements
- User data filtering by `request.user`
- No cross-user data leakage
- Appropriate use of LoginRequiredMixin

### Review Results

#### ✅ Users App (`users/views.py`)
**Public Views** (Intentionally public):
- `LoginView`: Public access required for authentication
- `SignupView`: Public access required for registration
- `CustomLogoutView`: Handles logout (no sensitive data)

**Protected Views**:
- `DashboardView`: Uses `LoginRequiredMixin` ✓
  - Filters: `Account.objects.filter(user=user)` ✓
  - Filters: `Transaction.objects.filter(account__user=user)` ✓
  - All queries properly filtered by authenticated user ✓

#### ✅ Accounts App (`accounts/views.py`)
All views use `LoginRequiredMixin` ✓

- `AccountListView`:
  - Filters: `Account.objects.filter(user=self.request.user)` ✓
  - Optimized with `select_related('user')` ✓

- `AccountCreateView`:
  - Sets: `form.instance.user = self.request.user` ✓
  - Associates account with authenticated user ✓

- `AccountUpdateView`:
  - Filters: `Account.objects.filter(user=self.request.user)` ✓
  - Prevents editing other users' accounts ✓

- `AccountDeleteView`:
  - Filters: `Account.objects.filter(user=self.request.user)` ✓
  - Prevents deleting other users' accounts ✓
  - Protected from deletion if transactions exist (ProtectedError) ✓

#### ✅ Categories App (`categories/views.py`)
All views use `LoginRequiredMixin` ✓

- `CategoryListView`:
  - Filters: `Category.objects.filter(user=self.request.user)` ✓
  - Optimized with `select_related('user')` ✓

- `CategoryCreateView`:
  - Sets: `form.instance.user = self.request.user` ✓
  - Associates category with authenticated user ✓

- `CategoryUpdateView`:
  - Filters: `Category.objects.filter(user=self.request.user)` ✓
  - Prevents editing other users' categories ✓

- `CategoryDeleteView`:
  - Filters: `Category.objects.filter(user=self.request.user)` ✓
  - Prevents deleting other users' categories ✓
  - Protected from deletion if transactions exist (ProtectedError) ✓

#### ✅ Transactions App (`transactions/views.py`)
All views use `LoginRequiredMixin` ✓

- `TransactionListView`:
  - Filters: `Transaction.objects.filter(account__user=self.request.user)` ✓
  - Optimized with `select_related('account', 'category')` ✓
  - Context filters: `Account.objects.filter(user=self.request.user)` ✓
  - Context filters: `Category.objects.filter(user=self.request.user)` ✓

- `TransactionCreateView`:
  - Form receives: `kwargs['user'] = self.request.user` ✓
  - Form filters accounts and categories by user ✓

- `TransactionUpdateView`:
  - Filters: `Transaction.objects.filter(account__user=self.request.user)` ✓
  - Form receives: `kwargs['user'] = self.request.user` ✓
  - Prevents editing other users' transactions ✓

- `TransactionDeleteView`:
  - Filters: `Transaction.objects.filter(account__user=self.request.user)` ✓
  - Prevents deleting other users' transactions ✓

#### ✅ Profiles App (`profiles/views.py`)
All views use `LoginRequiredMixin` ✓

- `ProfileDetailView`:
  - Overrides `get_object()`: Returns only current user's profile ✓
  - No pk in URL - always shows authenticated user's profile ✓

- `ProfileUpdateView`:
  - Overrides `get_object()`: Returns only current user's profile ✓
  - No pk in URL - always edits authenticated user's profile ✓

### Security Patterns Verified

✅ **Authentication**: All protected views use `LoginRequiredMixin`
✅ **Authorization**: All queries filter by `user=request.user` or `account__user=request.user`
✅ **Data Isolation**: No cross-user data leakage possible
✅ **Query Optimization**: Uses `select_related()` to prevent N+1 queries
✅ **Protected Deletions**: Accounts and Categories protected if transactions exist
✅ **Form Security**: User assignment happens server-side, not from form data

### Intentionally Public Views
The following views are intentionally accessible without authentication:
- `LoginView`: Required for users to authenticate
- `SignupView`: Required for new user registration
- `CustomLogoutView`: Handles logout, redirects to public home page

**Note**: The home page view (if exists) may also be public by design.

---

## 6. SQL Injection Protection (6.9.6)

### Verification Method
Searched entire codebase for:
- Raw SQL usage: `.raw()`, `.execute()`, `cursor()`
- Direct SQL query execution

### Results
**No raw SQL queries found** ✓

### Protection Mechanism
All database queries use Django ORM exclusively:
- `Model.objects.filter()`
- `Model.objects.get()`
- `Model.objects.create()`
- `.aggregate()`, `.annotate()`
- QuerySet methods with automatic parameterization

### How Django ORM Prevents SQL Injection
Django automatically escapes and parameterizes all values:

```python
# SECURE: Django ORM (used throughout Finanpy)
Account.objects.filter(name=user_input)
# Generates: SELECT * FROM accounts WHERE name = %s
# Parameters: [user_input]  -- safely escaped

# DANGEROUS: Raw SQL (NOT USED in Finanpy)
cursor.execute(f"SELECT * FROM accounts WHERE name = '{user_input}'")
# Vulnerable to: ' OR '1'='1
```

### Audit Findings
- ✅ Zero raw SQL queries in codebase
- ✅ All queries use Django ORM
- ✅ All parameters automatically escaped
- ✅ No string concatenation in queries
- ✅ No `.extra()` with unsafe SQL

### Recommendations
- **NEVER** use raw SQL without parameterization
- **ALWAYS** use Django ORM for queries
- If raw SQL is absolutely necessary (rare), use parameterized queries:
  ```python
  Model.objects.raw('SELECT * FROM table WHERE id = %s', [id])
  ```

---

## 7. XSS (Cross-Site Scripting) Protection (6.9.7)

### Verification Method
Searched entire codebase for:
- Unsafe template filters: `|safe`
- Disabled autoescaping: `{% autoescape off %}`

### Results
**No unsafe template operations found** ✓

### Protection Mechanism

#### Template Autoescaping (Enabled by Default)
Django automatically escapes all variables in templates:

```django
{# SECURE: Automatic escaping (used throughout Finanpy) #}
{{ account.name }}
{# If name = "<script>alert('xss')</script>" #}
{# Renders as: &lt;script&gt;alert('xss')&lt;/script&gt; #}

{# DANGEROUS: Manual bypass (NOT USED in Finanpy) #}
{{ account.name|safe }}
{# Would render actual <script> tag - VULNERABLE #}
```

#### Settings Verification
**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (lines 67-80)

Template configuration includes:
```python
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'OPTIONS': {
            'context_processors': [...],
            # Autoescaping is enabled by default (not explicitly disabled)
        },
    },
]
```

### Audit Findings
- ✅ No `|safe` filters in templates
- ✅ No `{% autoescape off %}` blocks
- ✅ Autoescaping enabled globally (Django default)
- ✅ All user input automatically escaped
- ✅ JSON data properly serialized with `json.dumps()`

### Templates Verified
All templates audited:
- `/Users/azambuja/projects/finanpy/templates/base.html`
- `/Users/azambuja/projects/finanpy/templates/dashboard.html`
- `/Users/azambuja/projects/finanpy/templates/auth/*.html`
- `/Users/azambuja/projects/finanpy/templates/accounts/*.html`
- `/Users/azambuja/projects/finanpy/templates/categories/*.html`
- `/Users/azambuja/projects/finanpy/templates/transactions/*.html`
- `/Users/azambuja/projects/finanpy/templates/profiles/*.html`

### Additional XSS Protections

**SECURE_BROWSER_XSS_FILTER** (Enabled)
```python
SECURE_BROWSER_XSS_FILTER = True
```
Enables browser's built-in XSS filtering as an additional layer.

**SECURE_CONTENT_TYPE_NOSNIFF** (Enabled)
```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```
Prevents browsers from MIME-sniffing responses, which could lead to XSS.

---

## Additional Security Headers

Beyond the Sprint 6.9 requirements, additional security headers are configured:

### X-Frame-Options: DENY
**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (line 187)

```python
X_FRAME_OPTIONS = 'DENY'
```

**Purpose**: Prevents the site from being embedded in iframes
**Protection**: Defends against clickjacking attacks
**Impact**: Site cannot be embedded in frames on other domains

### Content-Type Nosniff
**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (line 181)

```python
SECURE_CONTENT_TYPE_NOSNIFF = True
```

**Purpose**: Prevents MIME-sniffing attacks
**Protection**: Forces browsers to respect declared content types
**Impact**: Reduces risk of content-type confusion attacks

---

## Django Security Middleware

The following middleware provides additional security:

**Location**: `/Users/azambuja/projects/finanpy/core/settings.py` (lines 55-63)

```python
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',  # Security headers
    'django.contrib.sessions.middleware.SessionMiddleware',  # Session management
    'django.middleware.common.CommonMiddleware',  # Common utilities
    'django.middleware.csrf.CsrfViewMiddleware',  # CSRF protection
    'django.contrib.auth.middleware.AuthenticationMiddleware',  # Authentication
    'django.contrib.messages.middleware.MessageMiddleware',  # Messages
    'django.middleware.clickjacking.XFrameOptionsMiddleware',  # Clickjacking protection
]
```

All critical security middleware is properly configured and ordered.

---

## Deployment Security Checklist

### Pre-Deployment

- [ ] Generate strong SECRET_KEY (50+ random characters)
- [ ] Set DEBUG=False in production environment
- [ ] Configure ALLOWED_HOSTS with actual domain(s)
- [ ] Obtain and install SSL/TLS certificate
- [ ] Configure web server for HTTPS (Nginx/Apache/Load Balancer)
- [ ] Update .env file with production settings
- [ ] Review environment variables in .env.example
- [ ] Set up database backups (if using PostgreSQL/MySQL)

### Security Settings Verification

- [ ] SECURE_SSL_REDIRECT=True (after HTTPS is working)
- [ ] SESSION_COOKIE_SECURE=True
- [ ] CSRF_COOKIE_SECURE=True
- [ ] SECURE_HSTS_SECONDS=31536000 (start lower, increase gradually)
- [ ] SECURE_HSTS_INCLUDE_SUBDOMAINS=True (if applicable)
- [ ] SECURE_HSTS_PRELOAD=True (if submitting to preload list)

### Django Security Check

Run the deployment check command:
```bash
python manage.py check --deploy
```

**Expected in Development** (DEBUG=True):
- Warnings about security settings not enabled
- These are normal and will be resolved when DEBUG=False

**Expected in Production** (DEBUG=False):
- No warnings if all settings are properly configured
- Address any remaining warnings before going live

### Post-Deployment

- [ ] Verify HTTPS is working correctly
- [ ] Test all authentication flows
- [ ] Verify session persistence
- [ ] Test CSRF protection on forms
- [ ] Check browser security headers (use securityheaders.com)
- [ ] Verify HSTS headers are present
- [ ] Test cross-user data isolation
- [ ] Monitor application logs for security events

---

## Security Testing Commands

### Run Security Checks
```bash
# Full deployment security check
python manage.py check --deploy

# Run all checks
python manage.py check

# Database checks
python manage.py check --database default
```

### Verify Settings
```bash
# Django shell - check security settings
python manage.py shell

>>> from django.conf import settings
>>> settings.DEBUG  # Should be False in production
>>> settings.ALLOWED_HOSTS  # Should include your domain
>>> settings.SECRET_KEY[:10]  # Check length (don't print full key)
```

### Test HTTPS Locally (with self-signed cert)
```bash
# Install django-extensions
pip install django-extensions

# Run with SSL (self-signed)
python manage.py runserver_plus --cert-file cert.pem
```

---

## Security Incident Response

### If a Security Issue is Discovered

1. **Assess the Impact**
   - Determine scope of the issue
   - Identify affected users
   - Document the vulnerability

2. **Immediate Actions**
   - Disable affected functionality if critical
   - Rotate SECRET_KEY if compromised
   - Invalidate sessions if necessary
   - Notify affected users if data was exposed

3. **Remediation**
   - Apply security patches
   - Update dependencies
   - Review and fix vulnerable code
   - Deploy fixes immediately

4. **Post-Incident**
   - Conduct security audit
   - Update security documentation
   - Implement additional monitoring
   - Review access logs

### Reporting Security Issues

If you discover a security vulnerability:
- **DO NOT** open a public GitHub issue
- Email security contact privately (if configured)
- Provide detailed reproduction steps
- Allow time for patches before public disclosure

---

## Security Maintenance

### Regular Tasks

**Weekly**:
- Review application logs for anomalies
- Check for failed login attempts
- Monitor unusual data access patterns

**Monthly**:
- Update dependencies: `pip list --outdated`
- Review Django security releases
- Check for security advisories

**Quarterly**:
- Run comprehensive security audit
- Review and update security documentation
- Test incident response procedures
- Review user access permissions

### Dependency Security

```bash
# Check for security vulnerabilities in dependencies
pip install safety
safety check

# Update dependencies (test thoroughly after)
pip install --upgrade django
pip install --upgrade -r requirements.txt
```

---

## Conclusion

All security requirements for Sprint 6, Tarefa 6.9 have been successfully implemented and verified:

✅ **6.9.1**: SSL/HTTPS redirect configured
✅ **6.9.2**: Session cookie security enabled
✅ **6.9.3**: CSRF cookie security enabled
✅ **6.9.4**: HSTS configured with 1-year duration
✅ **6.9.5**: All views audited - proper authentication and authorization
✅ **6.9.6**: SQL injection protection verified - only ORM used
✅ **6.9.7**: XSS protection verified - autoescaping enabled

**Additional protections configured**:
- Content-Type nosniff
- XSS filter enabled
- Clickjacking protection (X-Frame-Options)
- CSRF middleware enabled
- Query optimization with select_related
- Protected deletions (accounts/categories with transactions)

The application follows Django security best practices and implements defense-in-depth strategies. All security settings are properly documented in `.env.example` and automatically activate in production when `DEBUG=False`.

---

**Document Version**: 1.0
**Last Updated**: 2025-10-26
**Sprint**: 6 - Tarefa 6.9
**Status**: ✅ Complete
