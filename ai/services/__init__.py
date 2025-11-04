'''
AI Services module for Finanpy.

This module contains business logic services for AI operations,
such as analysis generation and result processing.
'''

from ai.services.analysis_service import (
    generate_analysis_for_user,
    get_latest_analysis
)

__all__ = [
    'generate_analysis_for_user',
    'get_latest_analysis'
]
