from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()


class AIAnalysis(models.Model):
    '''
    Model to store AI-generated financial analysis for users.

    Each analysis is associated with a specific user and contains
    AI-generated insights, recommendations, and the period analyzed.
    '''
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        related_name='ai_analyses'
    )
    analysis_text = models.TextField(
        verbose_name='Texto da Análise',
        help_text='Análise financeira completa gerada pela IA'
    )
    key_insights = models.JSONField(
        default=list,
        verbose_name='Insights Principais',
        help_text='Lista de insights principais identificados pela IA'
    )
    recommendations = models.JSONField(
        default=list,
        verbose_name='Recomendações',
        help_text='Lista de recomendações geradas pela IA'
    )
    period_analyzed = models.CharField(
        max_length=100,
        verbose_name='Período Analisado',
        help_text='Período dos dados financeiros analisados'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Criado em'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Atualizado em'
    )

    class Meta:
        app_label = 'ai'
        verbose_name = 'Análise de IA'
        verbose_name_plural = 'Análises de IA'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        '''Return string representation with user email and creation date.'''
        return f'Análise de {self.user.email} - {self.created_at.strftime("%d/%m/%Y %H:%M")}'
