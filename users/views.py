import json
from datetime import datetime, timedelta
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import CreateView, FormView, TemplateView

from accounts.models import Account
from ai.models import AIAnalysis
from transactions.models import Transaction

from .forms import LoginForm, SignupForm


class LoginView(FormView):
    """
    View for user authentication with custom email-based login.

    Uses LoginForm with email (not username) as the identifier field.
    Validates credentials and logs in the user on success.
    Displays error messages for invalid credentials.
    """

    form_class = LoginForm
    template_name = 'auth/login.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """
        Process valid form submission and authenticate user.

        Attempts to authenticate user with provided email and password.
        On success: logs in user, displays success message, and redirects to dashboard.
        On failure: adds error to form and returns to login page.

        Args:
            form: The validated LoginForm instance

        Returns:
            HttpResponseRedirect: Redirect to success_url on valid credentials
            HttpResponse: Rendered form with errors on invalid credentials
        """
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        # Authenticate using email as username (CustomUser configuration)
        user = authenticate(self.request, username=email, password=password)

        if user is not None:
            # Valid credentials - log in user
            login(self.request, user)

            # Display success message
            messages.success(
                self.request,
                f'Bem-vindo de volta, {user.email}!'
            )

            return super().form_valid(form)
        else:
            # Invalid credentials - add error to form
            form.add_error(
                None,
                'Email ou senha incorretos. Por favor, tente novamente.'
            )
            return self.form_invalid(form)


class SignupView(CreateView):
    """
    View for user registration with automatic login after signup.

    Uses SignupForm for custom email-based authentication.
    After successful registration, automatically logs in the user
    and redirects to the dashboard.
    """

    form_class = SignupForm
    template_name = 'auth/signup.html'
    success_url = reverse_lazy('dashboard')

    def form_valid(self, form):
        """
        Process valid form submission.

        Saves the new user, automatically logs them in,
        displays success message, and redirects to dashboard.

        Args:
            form: The validated SignupForm instance

        Returns:
            HttpResponseRedirect: Redirect to success_url (dashboard)
        """
        response = super().form_valid(form)

        # Automatically log in the user after successful registration
        login(self.request, self.object)

        # Display success message
        messages.success(
            self.request,
            f'Bem-vindo ao Finanpy, {self.object.email}! Sua conta foi criada com sucesso.'
        )

        return response


class CustomLogoutView(DjangoLogoutView):
    """
    Custom logout view that adds a success message.

    Inherits from Django's LogoutView and overrides dispatch()
    to display a friendly success message before logging out.
    Redirects to LOGOUT_REDIRECT_URL configured in settings.
    """

    def dispatch(self, request, *args, **kwargs):
        """
        Override dispatch to add success message before logout.

        Args:
            request: The HTTP request object
            *args: Variable length argument list
            **kwargs: Arbitrary keyword arguments

        Returns:
            HttpResponseRedirect: Redirect to LOGOUT_REDIRECT_URL
        """
        messages.success(request, 'Você saiu da sua conta com sucesso. Até logo!')
        return super().dispatch(request, *args, **kwargs)


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Dashboard view for authenticated users.

    Displays comprehensive financial statistics including:
    - Total balance across all accounts
    - Current month income and expenses
    - Month balance (income - expenses)
    - Recent transactions (last 10)
    - Top 5 expense categories for the current month
    - Number of active accounts

    All data is filtered by the authenticated user for security.
    """

    template_name = 'dashboard.html'

    def get_context_data(self, **kwargs):
        """
        Calculate and add financial statistics to the template context.

        Performs optimized queries with select_related/prefetch_related
        to avoid N+1 queries. All monetary calculations use Decimal
        for precision.

        Args:
            **kwargs: Arbitrary keyword arguments

        Returns:
            dict: Context dictionary with comprehensive dashboard data
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Get current month date range
        now = datetime.now()
        current_month_start = now.replace(day=1)

        # 1. Calculate total balance across all user accounts
        total_balance_data = Account.objects.filter(
            user=user
        ).select_related('user').aggregate(
            total=Sum('balance')
        )
        total_balance = total_balance_data['total'] or Decimal('0.00')

        # 2. Calculate current month income
        month_income_data = Transaction.objects.filter(
            account__user=user,
            transaction_type=Transaction.TransactionType.INCOME,
            transaction_date__gte=current_month_start
        ).aggregate(
            total=Sum('amount')
        )
        month_income = month_income_data['total'] or Decimal('0.00')

        # 3. Calculate current month expenses
        month_expenses_data = Transaction.objects.filter(
            account__user=user,
            transaction_type=Transaction.TransactionType.EXPENSE,
            transaction_date__gte=current_month_start
        ).aggregate(
            total=Sum('amount')
        )
        month_expenses = month_expenses_data['total'] or Decimal('0.00')

        # 4. Calculate month balance (income - expenses)
        month_balance = month_income - month_expenses

        # 5. Get last 10 transactions with optimized queries
        recent_transactions = Transaction.objects.filter(
            account__user=user
        ).select_related(
            'account',
            'category'
        ).order_by(
            '-transaction_date',
            '-created_at'
        )[:10]

        # 6. Get top 5 expense categories for current month
        top_categories = Transaction.objects.filter(
            account__user=user,
            transaction_type=Transaction.TransactionType.EXPENSE,
            transaction_date__gte=current_month_start
        ).values(
            'category__name',
            'category__color'
        ).annotate(
            total_amount=Sum('amount')
        ).order_by(
            '-total_amount'
        )[:5]

        # 7. Count active accounts
        active_accounts_count = Account.objects.filter(
            user=user,
            is_active=True
        ).select_related('user').count()

        # 8. Prepare data for pie chart (category expense breakdown - current month)
        category_chart_data = []
        for cat in top_categories:
            category_chart_data.append({
                'name': cat['category__name'],
                'total': float(cat['total_amount']),
                'color': cat['category__color']
            })

        # 9. Prepare data for line chart (last 6 months income vs expense)
        month_labels = []
        income_data = []
        expense_data = []

        # Calculate data for last 6 months
        for i in range(5, -1, -1):
            # Calculate month start and end dates
            target_date = now - timedelta(days=30 * i)
            month_start = target_date.replace(day=1)

            # Calculate next month
            if month_start.month == 12:
                next_month_start = month_start.replace(year=month_start.year + 1, month=1)
            else:
                next_month_start = month_start.replace(month=month_start.month + 1)

            # Query income for this month
            month_inc = Transaction.objects.filter(
                account__user=user,
                transaction_type=Transaction.TransactionType.INCOME,
                transaction_date__gte=month_start,
                transaction_date__lt=next_month_start
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            # Query expenses for this month
            month_exp = Transaction.objects.filter(
                account__user=user,
                transaction_type=Transaction.TransactionType.EXPENSE,
                transaction_date__gte=month_start,
                transaction_date__lt=next_month_start
            ).aggregate(total=Sum('amount'))['total'] or Decimal('0.00')

            # Add to arrays
            month_labels.append(month_start.strftime('%b/%y'))
            income_data.append(float(month_inc))
            expense_data.append(float(month_exp))

        # Prepare monthly chart data as JSON
        monthly_chart_data = {
            'labels': month_labels,
            'income': income_data,
            'expense': expense_data
        }

        # Add all data to context
        context.update({
            'user': user,
            'total_balance': total_balance,
            'month_income': month_income,
            'month_expenses': month_expenses,
            'month_balance': month_balance,
            'recent_transactions': recent_transactions,
            'top_categories': top_categories,
            'active_accounts_count': active_accounts_count,
            'current_month': now.strftime('%B %Y'),
            'latest_analysis': AIAnalysis.objects.filter(
                user=user
            ).order_by('-created_at').first(),
            # Chart data
            'category_chart_data': json.dumps(category_chart_data),
            'monthly_chart_data': json.dumps(monthly_chart_data),
        })

        return context
