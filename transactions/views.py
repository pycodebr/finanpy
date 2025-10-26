from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.urls import reverse_lazy
from django.utils.dateparse import parse_date
from django.views.generic import CreateView, DeleteView, ListView, UpdateView

from accounts.models import Account
from categories.models import Category

from .forms import TransactionForm
from .models import Transaction


class TransactionListView(LoginRequiredMixin, ListView):
    """
    Lista as transações do usuário autenticado com filtros avançados.
    """

    model = Transaction
    template_name = 'transactions/transaction_list.html'
    context_object_name = 'transactions'
    paginate_by = 20

    def get_paginate_by(self, queryset):
        return self.request.GET.get('show', self.paginate_by)


    def dispatch(self, request, *args, **kwargs):
        self.filtered_queryset = Transaction.objects.none()
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Transaction.objects.filter(
            account__user=self.request.user
        ).select_related(
            'account',
            'category',
        )

        start_date = self.request.GET.get('data_inicio')
        end_date = self.request.GET.get('data_fim')
        account_id = self.request.GET.get('conta')
        category_id = self.request.GET.get('categoria')

        if start_date:
            parsed_start = parse_date(start_date)
            if parsed_start:
                queryset = queryset.filter(transaction_date__gte=parsed_start)

        if end_date:
            parsed_end = parse_date(end_date)
            if parsed_end:
                queryset = queryset.filter(transaction_date__lte=parsed_end)

        if account_id:
            queryset = queryset.filter(account_id=account_id)

        if category_id:
            queryset = queryset.filter(category_id=category_id)

        orderby = self.request.GET.get('orderby', '-transaction_date')
        queryset = queryset.order_by(orderby)

        self.filters = {
            'data_inicio': start_date,
            'data_fim': end_date,
            'conta': account_id,
            'categoria': category_id,
            'show': self.request.GET.get('show', self.paginate_by),
            'orderby': self.request.GET.get('orderby', '-transaction_date'),
        }
        self.filtered_queryset = queryset

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = getattr(self, 'filtered_queryset', Transaction.objects.none())

        income_total = queryset.filter(
            transaction_type=Transaction.TransactionType.INCOME
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        expense_total = queryset.filter(
            transaction_type=Transaction.TransactionType.EXPENSE
        ).aggregate(total=Sum('amount'))['total'] or Decimal('0')

        context.update({
            'accounts': Account.objects.filter(user=self.request.user).order_by('name'),
            'categories': Category.objects.filter(user=self.request.user).order_by('name'),
            'total_income': income_total,
            'total_expense': expense_total,
            'balance': income_total - expense_total,
            'filters': getattr(self, 'filters', {}),
            'has_filters': any(filter_value for filter_value in getattr(self, 'filters', {}).values()),
            'show': self.request.GET.get('show', self.paginate_by),
        })

        return context


class TransactionCreateView(LoginRequiredMixin, CreateView):
    """
    Cria uma nova transação para o usuário autenticado.
    """

    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')
    extra_context = {
        'page_title': 'Nova Transação',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        categories_qs = form.fields['category'].queryset if form else Category.objects.none()
        context.update({
            'categories_data': [
                {
                    'id': str(category.id),
                    'name': category.name,
                    'category_type': category.category_type,
                }
                for category in categories_qs
            ],
            'is_editing': False,
        })
        return context

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Check for balance warning (non-blocking)
        if hasattr(form, 'balance_warning') and form.balance_warning:
            messages.warning(self.request, form.balance_warning)
        messages.success(self.request, 'Transação criada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Corrija os erros abaixo para continuar.')
        return super().form_invalid(form)


class TransactionUpdateView(LoginRequiredMixin, UpdateView):
    """
    Atualiza uma transação existente do usuário.
    """

    model = Transaction
    form_class = TransactionForm
    template_name = 'transactions/transaction_form.html'
    success_url = reverse_lazy('transactions:transaction_list')
    extra_context = {
        'page_title': 'Editar Transação',
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = context.get('form')
        categories_qs = form.fields['category'].queryset if form else Category.objects.none()
        context.update({
            'categories_data': [
                {
                    'id': str(category.id),
                    'name': category.name,
                    'category_type': category.category_type,
                }
                for category in categories_qs
            ],
            'is_editing': True,
        })
        return context

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user).select_related(
            'account',
            'category',
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        # Check for balance warning (non-blocking)
        if hasattr(form, 'balance_warning') and form.balance_warning:
            messages.warning(self.request, form.balance_warning)
        messages.success(self.request, 'Transação atualizada com sucesso!')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Não foi possível atualizar a transação.')
        return super().form_invalid(form)


class TransactionDeleteView(LoginRequiredMixin, DeleteView):
    """
    Exclui uma transação do usuário autenticado.
    """

    model = Transaction
    template_name = 'transactions/transaction_confirm_delete.html'
    success_url = reverse_lazy('transactions:transaction_list')

    def get_queryset(self):
        return Transaction.objects.filter(account__user=self.request.user).select_related(
            'account',
            'category',
        )

    def delete(self, request, *args, **kwargs):
        """
        Handles the deletion of a transaction.

        This method attempts to delete the transaction and displays a success
        message upon completion.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        messages.success(self.request, "Transação excluída com sucesso!")
        return HttpResponseRedirect(success_url)
