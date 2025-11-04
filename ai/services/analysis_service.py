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
from datetime import timedelta
from typing import Optional

from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone

from ai.agents.finance_insight_agent import run_analysis
from ai.models import AIAnalysis


# Configure logging
logger = logging.getLogger(__name__)

# Get User model
User = get_user_model()


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
        logger.info(f'Starting analysis generation workflow for user_id={user_id}')

        # Task 8.8.6: Validate user exists
        try:
            user = User.objects.get(pk=user_id)
            logger.debug(f'User validated: {user.email} (id={user_id})')
        except User.DoesNotExist:
            logger.error(f'User with id={user_id} does not exist')
            raise ValueError(f'User with id {user_id} does not exist')

        # Task 8.8.7: Check if analysis exists and is recent (< 24 hours)
        cutoff_time = timezone.now() - timedelta(hours=24)
        existing_analysis = AIAnalysis.objects.filter(
            user=user,
            created_at__gte=cutoff_time
        ).order_by('-created_at').first()

        if existing_analysis:
            logger.info(
                f'Recent analysis found for user_id={user_id}, '
                f'created at {existing_analysis.created_at}. Returning existing analysis.'
            )
            return existing_analysis

        logger.info(f'No recent analysis found for user_id={user_id}. Generating new analysis.')

        # Task 8.8.8: Call agent to run analysis
        logger.debug(f'Invoking LangChain agent for user_id={user_id}')
        agent_result = run_analysis(user_id)

        # Task 8.8.9-8.8.10: Parse result dict
        # Agent returns: analysis_text, key_insights, recommendations, period_analyzed
        analysis_text = agent_result.get('analysis_text', '')
        key_insights = agent_result.get('key_insights', [])
        recommendations = agent_result.get('recommendations', [])
        period_analyzed = agent_result.get('period_analyzed', 'Últimos 30 dias')

        logger.debug(
            f'Agent result parsed for user_id={user_id}: '
            f'text_length={len(analysis_text)}, '
            f'insights={len(key_insights)}, '
            f'recommendations={len(recommendations)}'
        )

        # Validate parsed data
        if not analysis_text:
            logger.error(f'Agent returned empty analysis_text for user_id={user_id}')
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
        logger.info(
            f'Analysis successfully saved for user_id={user_id}, '
            f'analysis_id={analysis.pk}'
        )

        return analysis

    except ValueError as e:
        # Task 8.8.14: Exception handling - User not found
        logger.error(f'Validation error in generate_analysis_for_user: {str(e)}')
        raise

    except Exception as e:
        # Task 8.8.14: Exception handling - Agent execution or database errors
        logger.error(
            f'Error generating analysis for user_id={user_id}: {str(e)}',
            exc_info=True
        )
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
        logger.debug(f'Retrieving latest analysis for user_id={user_id}')

        # Task 8.8.15: Get most recent analysis for user
        latest_analysis = AIAnalysis.objects.filter(
            user_id=user_id
        ).order_by('-created_at').first()

        if latest_analysis:
            logger.info(
                f'Found latest analysis for user_id={user_id}, '
                f'created at {latest_analysis.created_at}'
            )
        else:
            logger.info(f'No analysis found for user_id={user_id}')

        return latest_analysis

    except Exception as e:
        logger.error(
            f'Error retrieving latest analysis for user_id={user_id}: {str(e)}',
            exc_info=True
        )
        raise Exception(f'Failed to retrieve latest analysis: {str(e)}')
