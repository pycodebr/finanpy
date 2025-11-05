'''
Analysis Service for orchestrating AI financial analysis.

This module provides the service layer for generating and managing AI-driven
financial analysis. It coordinates the LangChain agent execution, handles
database persistence, and enforces business rules like 24-hour analysis cooldown.

Main Functions:
    - generate_analysis_for_user: Generates new AI analysis for a user
    - get_latest_analysis: Retrieves the most recent analysis for a user
'''

import logging
import time
from datetime import timedelta
from typing import Optional

from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.db import transaction
from django.utils import timezone

from ai.agents.finance_insight_agent import run_analysis
from ai.models import AIAnalysis


# Configure logging
logger = logging.getLogger(__name__)

# Get User model
User = get_user_model()

CACHE_TTL_SECONDS = 60 * 60 * 24  # 24 hours


def _cache_key(user_id: int) -> str:
    return f'ai:analysis:{user_id}'


def _write_cache(analysis: AIAnalysis) -> None:
    cache.set(_cache_key(analysis.user_id), analysis.pk, CACHE_TTL_SECONDS)


def _read_cache(user_id: int) -> Optional[AIAnalysis]:
    cached_id = cache.get(_cache_key(user_id))
    if not cached_id:
        return None
    try:
        return AIAnalysis.objects.get(pk=cached_id)
    except AIAnalysis.DoesNotExist:
        cache.delete(_cache_key(user_id))
        return None


@transaction.atomic
def generate_analysis_for_user(user_id: int) -> AIAnalysis:
    '''
    Generate AI financial analysis for a specific user.

    This function orchestrates the complete analysis workflow:
    1. Validates user exists
    2. Checks if recent analysis exists (< 24 hours)
    3. Invokes LangChain agent to generate analysis
    4. Parses agent results
    5. Saves analysis to database

    Args:
        user_id (int): The ID of the user for whom to generate analysis.

    Returns:
        AIAnalysis: The generated (or existing if < 24h) analysis object.

    Raises:
        ValueError: If user_id is invalid or user does not exist.
        Exception: If agent execution or database operations fail.

    Example:
        >>> analysis = generate_analysis_for_user(user_id=5)
        >>> print(analysis.analysis_text)
        >>> print(f'Created at: {analysis.created_at}')

    Note:
        - Analysis is rate-limited to once per 24 hours per user
        - Uses Django transaction.atomic for database consistency
        - Comprehensive logging at INFO, DEBUG, and ERROR levels
        - Existing analysis within 24h is returned without regeneration
    '''
    try:
        logger.info('ai.analysis.start', extra={'user_id': user_id})

        # Task 8.8.6: Validate user exists
        try:
            user = User.objects.get(pk=user_id)
            logger.debug('ai.analysis.user_valid', extra={'user_id': user_id})
        except User.DoesNotExist:
            logger.error('ai.analysis.user_missing', extra={'user_id': user_id})
            raise ValueError(f'User with id {user_id} does not exist')

        cached_analysis = _read_cache(user_id)
        if cached_analysis:
            cached_analysis._ai_metadata = {'source': 'cache', 'elapsed_ms': 0}
            logger.info(
                'ai.analysis.cache_hit',
                extra={'user_id': user_id, 'analysis_id': cached_analysis.pk}
            )
            return cached_analysis

        # Task 8.8.7: Check if analysis exists and is recent (< 24 hours)
        cutoff_time = timezone.now() - timedelta(hours=24)
        existing_analysis = AIAnalysis.objects.filter(
            user=user,
            created_at__gte=cutoff_time
        ).order_by('-created_at').first()

        if existing_analysis:
            logger.info('ai.analysis.reuse_recent', extra={
                'user_id': user_id,
                'analysis_id': existing_analysis.pk,
                'created_at': existing_analysis.created_at.isoformat()
            })
            _write_cache(existing_analysis)
            existing_analysis._ai_metadata = {
                'source': 'recent',
                'created_at': existing_analysis.created_at.isoformat(),
                'elapsed_ms': 0
            }
            return existing_analysis

        logger.info('ai.analysis.generate_new', extra={'user_id': user_id})

        # Task 8.8.8: Call agent to run analysis
        logger.debug('ai.analysis.invoke_agent', extra={'user_id': user_id})
        started_at = time.perf_counter()
        agent_result = run_analysis(user_id)
        elapsed_ms = int((time.perf_counter() - started_at) * 1000)

        # Task 8.8.9-8.8.10: Parse result dict
        # Agent returns: analysis_text, key_insights, recommendations, period_analyzed
        analysis_text = agent_result.get('analysis_text', '')
        key_insights = agent_result.get('key_insights', [])
        recommendations = agent_result.get('recommendations', [])
        period_analyzed = agent_result.get('period_analyzed', 'Últimos 30 dias')
        metadata = agent_result.get('metadata', {}) or {}

        logger.debug('ai.analysis.agent_result', extra={
            'user_id': user_id,
            'text_length': len(analysis_text),
            'insights_count': len(key_insights),
            'recommendations_count': len(recommendations),
            'elapsed_ms': elapsed_ms,
            'model_latency_ms': metadata.get('model_latency_ms'),
            'input_tokens': metadata.get('input_tokens'),
            'output_tokens': metadata.get('output_tokens'),
            'source': metadata.get('source', 'agent')
        })

        # Validate parsed data
        if not analysis_text:
            logger.error('ai.analysis.empty_text', extra={'user_id': user_id})
            raise Exception('Agent generated empty analysis text')

        # Task 8.8.11: Create AIAnalysis object
        analysis = AIAnalysis(
            user=user,
            analysis_text=analysis_text,
            key_insights=key_insights,
            recommendations=recommendations,
            period_analyzed=period_analyzed
        )

        # Task 8.8.12: Save to database
        analysis.save()
        _write_cache(analysis)
        metadata.update({'elapsed_ms': elapsed_ms})
        logger.info('ai.analysis.completed', extra={
            'user_id': user_id,
            'analysis_id': analysis.pk,
            'elapsed_ms': metadata.get('elapsed_ms'),
            'source': metadata.get('source', 'agent'),
            'input_tokens': metadata.get('input_tokens'),
            'output_tokens': metadata.get('output_tokens'),
            'total_tokens': metadata.get('total_tokens')
        })
        analysis._ai_metadata = metadata

        return analysis

    except ValueError as e:
        # Task 8.8.14: Exception handling - User not found
        logger.error('ai.analysis.validation_error', extra={'user_id': user_id, 'error': str(e)})
        raise

    except Exception as e:
        # Task 8.8.14: Exception handling - Agent execution or database errors
        logger.error('ai.analysis.error', extra={'user_id': user_id, 'error': str(e)}, exc_info=True)
        raise Exception(f'Failed to generate analysis: {str(e)}')


def get_latest_analysis(user_id: int) -> Optional[AIAnalysis]:
    '''
    Retrieve the most recent AI analysis for a specific user.

    This function queries the database for the latest analysis object
    associated with the given user_id, regardless of when it was created.

    Args:
        user_id (int): The ID of the user whose latest analysis to retrieve.

    Returns:
        Optional[AIAnalysis]: The most recent AIAnalysis object if found,
                             None if no analysis exists for this user.

    Raises:
        Exception: If database query fails unexpectedly.

    Example:
        >>> latest = get_latest_analysis(user_id=5)
        >>> if latest:
        ...     print(f'Analysis from: {latest.created_at}')
        ... else:
        ...     print('No analysis found')

    Note:
        - Returns None if user has no analysis (not an error condition)
        - Does not validate if user exists (returns None for non-existent users)
        - Results are ordered by created_at descending
        - Uses database index on (user, created_at) for performance
    '''
    try:
        logger.debug('ai.analysis.retrieve_latest', extra={'user_id': user_id})

        # Task 8.8.15: Get most recent analysis for user
        latest_analysis = AIAnalysis.objects.filter(
            user_id=user_id
        ).order_by('-created_at').first()

        if latest_analysis:
            logger.info('ai.analysis.latest_found', extra={
                'user_id': user_id,
                'analysis_id': latest_analysis.pk,
                'created_at': latest_analysis.created_at.isoformat()
            })
        else:
            logger.info('ai.analysis.none_found', extra={'user_id': user_id})

        return latest_analysis

    except Exception as e:
        logger.error('ai.analysis.retrieve_error', extra={'user_id': user_id, 'error': str(e)}, exc_info=True)
        raise Exception(f'Failed to retrieve latest analysis: {str(e)}')
