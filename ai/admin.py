from django.contrib import admin

from ai.models import AIAnalysis


@admin.register(AIAnalysis)
class AIAnalysisAdmin(admin.ModelAdmin):
    '''
    Admin configuration for AIAnalysis model.

    Provides a user-friendly interface for viewing and managing AI-generated
    financial analyses with filtering, searching, and preview capabilities.
    '''

    list_display = [
        'user',
        'period_analyzed',
        'analysis_preview',
        'created_at',
    ]

    list_filter = [
        'created_at',
    ]

    search_fields = [
        'user__email',
        'analysis_text',
    ]

    readonly_fields = [
        'created_at',
        'updated_at',
    ]

    date_hierarchy = 'created_at'

    @admin.display(description='Preview da Análise')
    def analysis_preview(self, obj):
        '''
        Display a preview of the analysis text.

        Args:
            obj: AIAnalysis instance

        Returns:
            str: First 100 characters of analysis text with ellipsis if truncated
        '''
        if len(obj.analysis_text) > 100:
            return f'{obj.analysis_text[:100]}...'
        return obj.analysis_text
