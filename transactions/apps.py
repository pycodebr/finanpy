from django.apps import AppConfig


class TransactionsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'transactions'
    verbose_name = 'Transações'

    def ready(self):
        # Import signals to ensure account balances are kept in sync
        from . import signals  # noqa: F401
