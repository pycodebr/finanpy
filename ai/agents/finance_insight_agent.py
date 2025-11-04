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
import unicodedata
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
        Runnable: Configured LangChain agent ready to perform
                  financial analysis.

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
        model_name = _resolve_model_name()
        model = init_chat_model(
            model=f'openai:{model_name}',
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
            f'O user_id do usuario atual e {user_id}. '
            'Utilize exclusivamente as ferramentas fornecidas para coletar '
            'transacoes, contas, categorias, distribuicoes de gastos e comparativo '
            'de receitas versus despesas referentes aos ultimos 30 dias. '
            'Nao solicite dados adicionais ao usuario e nao interrompa o fluxo '
            'com perguntas. Depois de coletar os dados com as ferramentas, '
            'produza a analise final seguindo o formato solicitado na mensagem '
            'do sistema, incluindo visao geral, insights numericos e recomendacoes acionaveis.'
        )

        logger.debug(f'Invoking agent with request for user_id={user_id}')

        # Invoke the agent with the analysis request
        response = agent.invoke({'input': analysis_request})

        # Extract the analysis text from the response
        analysis_text = ''

        # Primary source: direct output field from agent executor
        output_text = response.get('output')
        if isinstance(output_text, str):
            analysis_text = output_text.strip()
        elif isinstance(output_text, list):
            analysis_text = ''.join(
                str(part) for part in output_text if part
            ).strip()

        # Fallback: last message returned by the agent run
        if not analysis_text:
            messages = response.get('messages', [])
            if not messages:
                logger.error(f'No messages in agent response for user_id={user_id}')
                raise Exception('Agent returned empty response')

            last_message = messages[-1]
            message_content = getattr(last_message, 'content', '') or getattr(last_message, 'text', '')

            if isinstance(message_content, str):
                analysis_text = message_content.strip()
            elif isinstance(message_content, list):
                parts = []
                for chunk in message_content:
                    if isinstance(chunk, str):
                        parts.append(chunk)
                    elif isinstance(chunk, dict):
                        text_content = chunk.get('text') or chunk.get('content')
                        if text_content:
                            parts.append(str(text_content))
                analysis_text = ''.join(parts).strip()
            else:
                analysis_text = str(message_content).strip()

        if not analysis_text:
            logger.error(
                f'Empty analysis text for user_id={user_id}. Raw response keys: {list(response.keys())}'
            )
            raise Exception('Agent generated empty analysis')

        logger.info(f'Agent analysis completed for user_id={user_id}, length={len(analysis_text)} chars')

        # Extract insights and recommendations from the text
        key_insights = _extract_insights(analysis_text)
        recommendations = _extract_recommendations(analysis_text)

        normalized_text = _normalize_text(analysis_text)
        if (
            'visao geral' not in normalized_text
            or not key_insights
            or not recommendations
        ):
            logger.warning(
                'Agent output missing expected sections for user_id=%s. '
                'Invoking fallback synthesis.',
                user_id
            )
            return _generate_fallback_analysis(user_id)

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


def _resolve_model_name() -> str:
    '''
    Resolve the OpenAI model name, falling back to gpt-4o-mini for reasoning-heavy models.
    '''
    configured = getattr(settings, 'AI_MODEL', 'gpt-4o-mini') or 'gpt-4o-mini'
    if isinstance(configured, str) and configured.lower().startswith('gpt-5'):
        logger.warning(
            'Configured model %s uses reasoning tokens extensively. Falling back to gpt-4o-mini for output generation.',
            configured
        )
        return 'gpt-4o-mini'
    return configured


def _normalize_text(text: str) -> str:
    '''
    Normalize text by removing accents and converting to lowercase.
    '''
    normalized = unicodedata.normalize('NFKD', text or '')
    stripped = ''.join(char for char in normalized if not unicodedata.combining(char))
    return stripped.lower()


def _generate_fallback_analysis(user_id: int) -> Dict:
    '''
    Generate analysis directly by collecting data with tools and prompting the LLM.
    '''
    logger.info('Running fallback analysis pipeline for user_id=%s', user_id)

    transactions = get_user_transactions.invoke({'user_id': user_id}) or []
    accounts = get_user_accounts.invoke({'user_id': user_id}) or []
    categories = get_user_categories.invoke({'user_id': user_id}) or []
    spending = get_spending_by_category.invoke({'user_id': user_id}) or []
    income_overview = get_income_vs_expense.invoke({'user_id': user_id}) or {}

    total_accounts = len(accounts)
    active_accounts = sum(1 for account in accounts if account.get('is_active'))
    total_balance = sum(account.get('balance', 0) for account in accounts)

    expense_transactions = [txn for txn in transactions if txn.get('type') == 'EXPENSE']
    income_transactions = [txn for txn in transactions if txn.get('type') == 'INCOME']

    total_income = sum(txn.get('amount', 0) for txn in income_transactions) or 0
    total_expense = sum(txn.get('amount', 0) for txn in expense_transactions) or 0
    balance = total_income - total_expense

    top_expenses = sorted(expense_transactions, key=lambda txn: txn.get('amount', 0), reverse=True)[:5]
    top_incomes = sorted(income_transactions, key=lambda txn: txn.get('amount', 0), reverse=True)[:5]

    summary_lines: List[str] = []
    summary_lines.append('Dados sintetizados automaticamente para o usuario (ultimos 30 dias):')
    summary_lines.append(f'- Contas ativas: {active_accounts}/{total_accounts} | saldo total aproximado: R$ {total_balance:,.2f}')
    summary_lines.append(
        f'- Receitas registradas: R$ {total_income:,.2f} em {len(income_transactions)} transacoes'
    )
    summary_lines.append(
        f'- Despesas registradas: R$ {total_expense:,.2f} em {len(expense_transactions)} transacoes'
    )
    summary_lines.append(f'- Saldo acumulado do periodo: R$ {balance:,.2f}')
    summary_lines.append('')

    summary_lines.append('Gastos por categoria (top 5):')
    if spending:
        for item in spending[:5]:
            summary_lines.append(
                f"- {item.get('category')}: R$ {item.get('total', 0):,.2f} "
                f"({item.get('percentage', 0)}% das despesas, {item.get('transaction_count', 0)} transacoes)"
            )
    else:
        summary_lines.append('- Sem despesas registradas.')
    summary_lines.append('')

    summary_lines.append('Maiores despesas individuais (top 5):')
    if top_expenses:
        for txn in top_expenses:
            summary_lines.append(
                f"- {txn.get('date')} | {txn.get('category')} | R$ {txn.get('amount', 0):,.2f} | conta {txn.get('account')}"
            )
    else:
        summary_lines.append('- Nenhuma despesa encontrada.')
    summary_lines.append('')

    summary_lines.append('Maiores receitas individuais (top 5):')
    if top_incomes:
        for txn in top_incomes:
            summary_lines.append(
                f"- {txn.get('date')} | {txn.get('category')} | R$ {txn.get('amount', 0):,.2f} | conta {txn.get('account')}"
            )
    else:
        summary_lines.append('- Nenhuma receita encontrada.')
    summary_lines.append('')

    summary_lines.append('Categorias cadastradas por tipo (quantidades):')
    if categories:
        income_categories = sum(1 for category in categories if category.get('type') == 'INCOME')
        expense_categories = sum(1 for category in categories if category.get('type') == 'EXPENSE')
        summary_lines.append(f'- Categorias de receita: {income_categories}')
        summary_lines.append(f'- Categorias de despesa: {expense_categories}')
    else:
        summary_lines.append('- Nenhuma categoria cadastrada.')
    summary_lines.append('')

    summary_lines.append(
        'Instrucao para o modelo: elabore a analise final com visao geral, insights e recomendacoes, '
        'sem pedir dados adicionais. Responda em ate 350 tokens e mantenha foco em acoes praticas.'
    )

    manual_prompt = '\n'.join(summary_lines)

    model_name = _resolve_model_name()
    model = init_chat_model(
        model=f'openai:{model_name}',
        temperature=min(settings.AI_TEMPERATURE, 0.7),
        max_tokens=min(settings.AI_MAX_TOKENS, 800),
        api_key=settings.OPENAI_API_KEY
    )

    response = model.invoke([
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': manual_prompt}
    ])

    manual_text = getattr(response, 'content', None) or getattr(response, 'text', None) or str(response)
    manual_text = manual_text.strip()

    if not manual_text:
        logger.error('Fallback analysis returned empty response for user_id=%s', user_id)
        raise Exception('Fallback analysis generated empty result')

    key_insights = _extract_insights(manual_text)
    recommendations = _extract_recommendations(manual_text)

    return {
        'analysis_text': manual_text,
        'key_insights': key_insights,
        'recommendations': recommendations,
        'period_analyzed': 'Últimos 30 dias'
    }


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
                r'(?:^|\n)(?:[-*•]|\d+[.)])\s*(.+?)(?=\n(?:[-*•]|\d+[.)])|\n\n|$)',
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
            items = re.findall(
                r'(?:^|\n)(?:[-*•]|\d+[.)])\s*(.+?)(?=\n|$)',
                first_half,
                re.MULTILINE
            )
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
                r'(?:^|\n)(?:[-*•]|\d+[.)])\s*(.+?)(?=\n(?:[-*•]|\d+[.)])|\n\n|$)',
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
            items = re.findall(
                r'(?:^|\n)(?:[-*•]|\d+[.)])\s*(.+?)(?=\n|$)',
                second_half,
                re.MULTILINE
            )
            recommendations = [item.strip() for item in items[:5] if item.strip()]

        logger.debug(f'Extracted {len(recommendations)} recommendations from analysis text')

    except Exception as e:
        logger.error(f'Error extracting recommendations: {str(e)}')

    return recommendations[:5]  # Return max 5 recommendations
