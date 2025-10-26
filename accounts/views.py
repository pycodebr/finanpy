from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.db.models.deletion import ProtectedError
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from .forms import AccountForm
from .models import Account


class AccountListView(LoginRequiredMixin, ListView):
    """
    Display a list of all accounts belonging to the authenticated user.

    Includes calculation of total balance across all accounts.
    Accounts are ordered alphabetically by name.
    """
    model = Account
    template_name = 'accounts/account_list.html'
    context_object_name = 'accounts'
    paginate_by = 9

    def get_queryset(self):
        """
        Filter accounts to show only those belonging to the current user.
        Orders results by account name.
        """
        return Account.objects.filter(
            user=self.request.user
        ).order_by('name')

    def get_context_data(self, **kwargs):
        """
        Add total balance calculation to the context.

        Calculates the sum of all account balances for the current user.
        """
        context = super().get_context_data(**kwargs)

        # Calculate total balance across all user accounts
        total_balance = Account.objects.filter(
            user=self.request.user
        ).aggregate(
            total=Sum('balance')
        )['total'] or 0

        context['total_balance'] = total_balance
        context['accounts_count'] = self.get_queryset().count()
        context['accounts_active_count'] = self.get_queryset().filter(is_active=True).count()
        last_updated_account = self.get_queryset().order_by('-updated_at').first()
        context['last_updated'] = last_updated_account.updated_at if last_updated_account else None

        return context


class AccountCreateView(LoginRequiredMixin, CreateView):
    """
    View for creating a new bank account.

    Requires user authentication and automatically associates the account
    with the authenticated user. Displays a success message upon successful
    account creation.
    """
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:account_list')
    extra_context = {
        'page_title': 'Nova Conta',
    }

    def form_valid(self, form):
        """
        Associate the account with the current user before saving.

        Args:
            form: The validated AccountForm instance

        Returns:
            HttpResponse: Redirect to success_url after saving
        """
        form.instance.user = self.request.user
        messages.success(self.request, 'Conta criada com sucesso!')
        return super().form_valid(form)


class AccountUpdateView(LoginRequiredMixin, UpdateView):
    """
    View for updating an existing bank account.

    Requires user authentication and ensures users can only edit their own
    accounts through queryset filtering. Displays a success message upon
    successful update.
    """
    model = Account
    form_class = AccountForm
    template_name = 'accounts/account_form.html'
    success_url = reverse_lazy('accounts:account_list')
    extra_context = {
        'page_title': 'Editar Conta',
    }

    def get_queryset(self):
        """
        Filter queryset to only include accounts belonging to the current user.

        Returns:
            QuerySet: Filtered Account queryset for the authenticated user
        """
        return Account.objects.filter(user=self.request.user)

    def form_valid(self, form):
        """
        Display success message after successful account update.

        Args:
            form: The validated AccountForm instance

        Returns:
            HttpResponse: Redirect to success_url after saving
        """
        messages.success(self.request, 'Conta atualizada com sucesso!')
        return super().form_valid(form)


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    """
    View for deleting a bank account.

    Requires user authentication and ensures users can only delete their own
    accounts through queryset filtering. Validates that the account has no
    associated transactions before allowing deletion. Displays appropriate
    error or success messages.
    """
    model = Account
    template_name = 'accounts/account_confirm_delete.html'
    success_url = reverse_lazy('accounts:account_list')

    def get_queryset(self):
        """
        Filter queryset to only include accounts belonging to the current user.

        Returns:
            QuerySet: Filtered Account queryset for the authenticated user
        """
        return Account.objects.filter(user=self.request.user)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        success_url = self.get_success_url()
        try:
            self.object.delete()
            messages.success(request, "Conta excluída com sucesso!")
            return HttpResponseRedirect(success_url)
        except ProtectedError:
            messages.error(
                request,
                "Não é possível excluir esta conta, pois existem transações associadas a ela."
            )
            return HttpResponseRedirect(success_url)
