'''
LangChain Finance Insight Agent for analyzing user financial data.

This module provides an AI agent that analyzes user transactions, accounts,
and spending patterns to generate personalized financial insights and
recommendations using OpenAI GPT models.

The agent uses database tools to access financial data and generates
comprehensive analysis in Portuguese with a friendly, motivating tone.
'''

import logging
import re
from typing import Dict, List

from django.conf import settings

from langchain.agents import create_agent
from langchain.chat_models import init_chat_model

from ai.tools.database_tools import (
    get_user_transactions,
    get_user_accounts,
    get_user_categories,
    get_spending_by_category,
    get_income_vs_expense
)


# Configure logging
logger = logging.getLogger(__name__)


# System prompt for the finance agent
SYSTEM_PROMPT = '''Você é um assistente financeiro pessoal especializado em análise de gastos.

Analise os dados financeiros do usuário e forneça uma análise completa e estruturada:

1. **Visão Geral**: Resumo claro e objetivo da situação financeira
2. **Insights Principais**: 3-5 insights específicos sobre padrões de gasto, categorias com maior impacto, tendências observadas
3. **Recomendações**: 3-5 recomendações práticas e acionáveis para melhorar a saúde financeira

**Diretrizes de Estilo**:
- Use tom amigável e motivador em português brasileiro
- Seja específico e use números reais dos dados
- Use emojis para tornar a leitura mais agradável
- Evite jargões técnicos complexos
- Foque em ações concretas que o usuário pode tomar

**Formato de Saída**:
Estruture sua resposta em seções claras, use bullet points quando apropriado, e certifique-se de que cada insight e recomendação seja específico aos dados do usuário.
'''


def initialize_agent(user_id: int):
    '''
    Initialize the LangChain finance insight agent for a specific user.

    This function creates and configures an agent with access to financial
    database tools and the OpenAI language model. The agent is pre-configured
    with a system prompt specialized in financial analysis.

    Args:
        user_id (int): The ID of the user for whom to create the agent.
                      This will be passed to all tool calls for data isolation.

    Returns:
        Agent: Configured LangChain agent ready to perform financial analysis.

    Raises:
        ValueError: If OPENAI_API_KEY is not configured in Django settings.
        Exception: If agent initialization fails for any reason.

    Example:
        >>> agent = initialize_agent(user_id=5)
        >>> result = agent.invoke({'messages': [{'role': 'user', 'content': 'Analyze my finances'}]})

    Note:
        - Requires OPENAI_API_KEY, AI_MODEL, AI_TEMPERATURE, and AI_MAX_TOKENS
          in Django settings
        - Agent has access to 5 tools: transactions, accounts, categories,
          spending by category, and income vs expense
        - All tools automatically filter data by user_id for security
    '''
    try:
        # Validate API key is configured
        if not settings.OPENAI_API_KEY:
            logger.error('OPENAI_API_KEY not configured in Django settings')
            raise ValueError('OPENAI_API_KEY is required but not configured')

        logger.info(f'Initializing finance insight agent for user_id={user_id}')

        # Create list of tools available to the agent
        tools = [
            get_user_transactions,
            get_user_accounts,
            get_user_categories,
            get_spending_by_category,
            get_income_vs_expense
        ]

        # Initialize chat model with OpenAI configuration
        # This allows us to pass temperature, max_tokens, and API key
        model = init_chat_model(
            model=f'openai:{settings.AI_MODEL}',
            temperature=settings.AI_TEMPERATURE,
            max_tokens=settings.AI_MAX_TOKENS,
            api_key=settings.OPENAI_API_KEY
        )

        # Create agent with configured model
        agent = create_agent(
            model=model,
            tools=tools,
            system_prompt=SYSTEM_PROMPT
        )

        logger.info(f'Agent successfully initialized for user_id={user_id}')
        return agent

    except ValueError as e:
        logger.error(f'Configuration error initializing agent: {str(e)}')
        raise

    except Exception as e:
        logger.error(f'Unexpected error initializing agent for user_id={user_id}: {str(e)}')
        raise Exception(f'Failed to initialize agent: {str(e)}')


def run_analysis(user_id: int) -> Dict:
    '''
    Run financial analysis for a specific user using the LangChain agent.

    This function initializes the agent, executes the analysis by invoking
    all necessary tools to gather financial data, and processes the AI's
    response into a structured format.

    Args:
        user_id (int): The ID of the user whose finances should be analyzed.

    Returns:
        Dict: Analysis results with the following keys:
            - analysis_text (str): Full analysis text generated by the AI
            - key_insights (List[str]): List of 3-5 key insights extracted
            - recommendations (List[str]): List of 3-5 recommendations extracted
            - period_analyzed (str): Description of the analyzed period

    Raises:
        ValueError: If user_id is invalid or API key not configured.
        Exception: If analysis fails due to OpenAI API errors or other issues.

    Example:
        >>> result = run_analysis(user_id=5)
        >>> print(result['analysis_text'])
        >>> for insight in result['key_insights']:
        ...     print(f'- {insight}')

    Note:
        - Analysis covers the last 30 days of financial data
        - Requires active OpenAI API key with sufficient credits
        - May take 10-30 seconds depending on data volume
        - Automatically handles missing data scenarios gracefully
    '''
    try:
        logger.info(f'Starting financial analysis for user_id={user_id}')

        # Initialize the agent
        agent = initialize_agent(user_id)

        # Create the analysis request
        analysis_request = (
            f'Analise os dados financeiros do usuário {user_id}. '
            'Use as ferramentas disponíveis para obter informações sobre '
            'transações, contas, categorias e padrões de gastos. '
            'Forneça uma análise completa com insights e recomendações.'
        )

        logger.debug(f'Invoking agent with request for user_id={user_id}')

        # Invoke the agent
        response = agent.invoke({
            'messages': [
                {'role': 'user', 'content': analysis_request}
            ]
        })

        # Extract the analysis text from the response
        # In LangChain v1.0, the response structure includes messages
        messages = response.get('messages', [])
        if not messages:
            logger.error(f'No messages in agent response for user_id={user_id}')
            raise Exception('Agent returned empty response')

        # Get the last message which contains the final analysis
        last_message = messages[-1]
        analysis_text = last_message.content if hasattr(last_message, 'content') else str(last_message)

        if not analysis_text:
            logger.error(f'Empty analysis text for user_id={user_id}')
            raise Exception('Agent generated empty analysis')

        logger.info(f'Agent analysis completed for user_id={user_id}, length={len(analysis_text)} chars')

        # Extract insights and recommendations from the text
        key_insights = _extract_insights(analysis_text)
        recommendations = _extract_recommendations(analysis_text)

        # Build structured result
        result = {
            'analysis_text': analysis_text,
            'key_insights': key_insights,
            'recommendations': recommendations,
            'period_analyzed': 'Últimos 30 dias'
        }

        logger.info(
            f'Analysis completed for user_id={user_id}: '
            f'{len(key_insights)} insights, {len(recommendations)} recommendations'
        )

        return result

    except ValueError as e:
        logger.error(f'Configuration error running analysis for user_id={user_id}: {str(e)}')
        raise

    except Exception as e:
        logger.error(f'Error running analysis for user_id={user_id}: {str(e)}')
        raise Exception(f'Failed to run financial analysis: {str(e)}')


def _extract_insights(text: str) -> List[str]:
    '''
    Extract key insights from the agent's analysis text.

    Attempts to parse the analysis text to identify and extract the key
    insights section. Looks for common patterns like bullet points,
    numbered lists, or section headers.

    Args:
        text (str): The full analysis text from the agent.

    Returns:
        List[str]: List of extracted insights (3-5 items typically).
                  Returns empty list if no insights can be extracted.

    Note:
        - Uses regex patterns to identify insight sections
        - Handles various formatting styles (bullets, numbers, emojis)
        - Cleans up extracted text (removes markers, extra whitespace)
    '''
    insights = []

    try:
        # Look for insights section
        # Common patterns: "Insights Principais", "Insights", etc.
        insights_pattern = r'(?:Insights?\s*Principais?|Principais?\s*Insights?)[:\s]*\n(.*?)(?=\n\n|\n[#*]|$)'
        insights_match = re.search(insights_pattern, text, re.IGNORECASE | re.DOTALL)

        if insights_match:
            insights_section = insights_match.group(1)

            # Extract bullet points or numbered items
            # Patterns: "- item", "* item", "1. item", "• item", emoji items
            items = re.findall(
                r'(?:^|\n)(?:[-*•]|\d+\.)\s*(.+?)(?=\n[-*•\d]|\n\n|$)',
                insights_section,
                re.MULTILINE
            )

            # Clean up extracted items
            insights = [item.strip() for item in items if item.strip()]

        # If no structured insights found, try to extract from context
        if not insights:
            logger.warning('Could not extract structured insights, attempting fallback')
            # Look for any bullet points in the first half of text
            first_half = text[:len(text)//2]
            items = re.findall(r'(?:^|\n)[-*•]\s*(.+?)(?=\n|$)', first_half, re.MULTILINE)
            insights = [item.strip() for item in items[:5] if item.strip()]

        logger.debug(f'Extracted {len(insights)} insights from analysis text')

    except Exception as e:
        logger.error(f'Error extracting insights: {str(e)}')

    return insights[:5]  # Return max 5 insights


def _extract_recommendations(text: str) -> List[str]:
    '''
    Extract recommendations from the agent's analysis text.

    Attempts to parse the analysis text to identify and extract the
    recommendations section. Looks for common patterns like bullet points,
    numbered lists, or section headers.

    Args:
        text (str): The full analysis text from the agent.

    Returns:
        List[str]: List of extracted recommendations (3-5 items typically).
                  Returns empty list if no recommendations can be extracted.

    Note:
        - Uses regex patterns to identify recommendation sections
        - Handles various formatting styles (bullets, numbers, emojis)
        - Cleans up extracted text (removes markers, extra whitespace)
    '''
    recommendations = []

    try:
        # Look for recommendations section
        # Common patterns: "Recomendações", "Sugestões", etc.
        rec_pattern = r'(?:Recomenda[çc][õo]es?|Sugest[õo]es?)[:\s]*\n(.*?)(?=\n\n|\n[#*]|$)'
        rec_match = re.search(rec_pattern, text, re.IGNORECASE | re.DOTALL)

        if rec_match:
            rec_section = rec_match.group(1)

            # Extract bullet points or numbered items
            items = re.findall(
                r'(?:^|\n)(?:[-*•]|\d+\.)\s*(.+?)(?=\n[-*•\d]|\n\n|$)',
                rec_section,
                re.MULTILINE
            )

            # Clean up extracted items
            recommendations = [item.strip() for item in items if item.strip()]

        # If no structured recommendations found, try to extract from context
        if not recommendations:
            logger.warning('Could not extract structured recommendations, attempting fallback')
            # Look for any bullet points in the second half of text
            second_half = text[len(text)//2:]
            items = re.findall(r'(?:^|\n)[-*•]\s*(.+?)(?=\n|$)', second_half, re.MULTILINE)
            recommendations = [item.strip() for item in items[:5] if item.strip()]

        logger.debug(f'Extracted {len(recommendations)} recommendations from analysis text')

    except Exception as e:
        logger.error(f'Error extracting recommendations: {str(e)}')

    return recommendations[:5]  # Return max 5 recommendations
