'''
Management command to trigger AI financial analysis generation.

This command allows running the AI analysis workflow for a single user
identified by email or for all active users. It leverages the service layer
implemented in `ai.services.analysis_service.generate_analysis_for_user`
to orchestrate the LangChain agent execution and persistence.
'''

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.utils import timezone

from ai.services.analysis_service import generate_analysis_for_user


class Command(BaseCommand):
    help = (
        'Executa a analise financeira inteligente para um usuario especifico '
        'ou para todos os usuarios ativos, respeitando o intervalo minimo de 24 horas.'
    )

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            '--user-email',
            type=str,
            help='E-mail do usuario para o qual a analise sera executada.'
        )
        parser.add_argument(
            '--all',
            action='store_true',
            help='Executa a analise para todos os usuarios ativos.'
        )

    def handle(self, *args, **options):
        user_email = options.get('user_email')
        process_all = options.get('all')

        if not user_email and not process_all:
            raise CommandError('Informe --user-email ou utilize --all para processar todos os usuarios.')

        if user_email and process_all:
            raise CommandError('Nao e possivel utilizar --user-email e --all simultaneamente.')

        User = get_user_model()

        if user_email:
            self._process_single_user(User, user_email)
            return

        self._process_all_users(User)

    def _process_single_user(self, User, user_email: str) -> None:
        try:
            user = User.objects.get(email=user_email, is_active=True)
        except User.DoesNotExist as exc:
            raise CommandError(f'Usuario ativo com e-mail {user_email} nao encontrado.') from exc

        self.stdout.write(self.style.MIGRATE_HEADING(f'Gerando analise financeira para {user.email}'))
        try:
            analysis = generate_analysis_for_user(user.pk)
        except ValueError as exc:
            raise CommandError(str(exc)) from exc
        except Exception as exc:
            raise CommandError(f'Falha ao gerar analise: {exc}') from exc

        created_at = timezone.localtime(analysis.created_at).strftime('%d/%m/%Y %H:%M')
        self.stdout.write(
            self.style.SUCCESS(
                f'Analise disponivel para {user.email} (gerada/em cache em {created_at}).'
            )
        )

    def _process_all_users(self, User) -> None:
        users = User.objects.filter(is_active=True).order_by('id')
        total = users.count()

        if total == 0:
            self.stdout.write(self.style.WARNING('Nenhum usuario ativo encontrado para processamento.'))
            return

        self.stdout.write(
            self.style.MIGRATE_HEADING(f'Processando analises financeiras para {total} usuario(s) ativo(s).')
        )

        processed = 0
        for index, user in enumerate(users, start=1):
            try:
                analysis = generate_analysis_for_user(user.pk)
            except ValueError as exc:
                self.stderr.write(self.style.ERROR(f'[{index}/{total}] {user.email}: {exc}'))
                continue
            except Exception as exc:
                self.stderr.write(
                    self.style.ERROR(f'[{index}/{total}] {user.email}: falha ao gerar analise ({exc}).')
                )
                continue

            processed += 1
            created_at = timezone.localtime(analysis.created_at).strftime('%d/%m/%Y %H:%M')
            self.stdout.write(
                self.style.SUCCESS(
                    f'[{index}/{total}] {user.email}: analise disponivel (gerada/em cache em {created_at}).'
                )
            )

        self.stdout.write(
            self.style.SUCCESS(
                f'Processamento concluido: {processed} de {total} usuarios processados com sucesso.'
            )
        )
