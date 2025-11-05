# AI Integration Expert

## Visão Geral do Papel
O **AI Integration Expert** é responsável por projetar, implementar e manter integrações de Inteligência Artificial no Finanpy. Esse papel garante que agentes LangChain utilizem os dados com segurança, entreguem análises confiáveis e respeitem políticas de privacidade e de produto. Atua como ponte entre backend, product e segurança quando o assunto é IA.

## LangChain 1.0 - Conceitos Fundamentais
- **Agents**: Orquestradores que decidem quais ferramentas (tools) executar para responder a uma pergunta.
- **Tools**: Funções Python decoradas com `@tool` que encapsulam acesso a dados ou operações específicas.
- **Prompt Templates**: Mensagens estruturadas que guiam o comportamento do modelo.
- **Executors**: Responsáveis por rodar o agente (ex.: `create_agent` + `invoke`).
- **Callbacks / Metadata**: Permitem coletar métricas (tokens, tempo) e logs.

## Padrões de Integração com Django
1. **Isolamento de Usuário**: Toda tool deve receber `user_id` e filtrar dados pelo usuário autenticado.
2. **Validação**: Use `_validate_user_id` para garantir que o usuário existe e está ativo.
3. **Performace**: Utilize `select_related`, `only` e limites (`[:N]`) para evitar consultas custosas.
4. **Resiliência**: Envolva chamadas da IA em `try/except` e implemente fallback seguro.
5. **Cache**: Use `django.core.cache` para reutilizar análises recentes (TTL padrão: 24h).

## Como Criar Tools para Acesso a Dados
1. Crie a função no módulo `ai/tools/database_tools.py`.
2. Valide o `user_id` com `_validate_user_id`.
3. Filtre dados com Django ORM e otimize consultas.
4. Converta o resultado para tipos primitivos (dict/list/float).
5. Decore a função com `@tool` e adicione docstring detalhada.
6. Retorne listas ou dicionários amigáveis ao LLM.

## Design de Prompts Eficazes
- **Contexto**: Explique claramente o papel do agente e o formato de saída desejado.
- **Segurança**: Instrua o modelo a não solicitar dados extras nem comentar sobre outros usuários.
- **Tom**: Especifique linguagem positiva, amigável e em português brasileiro.
- **Formato**: Indique seções, uso de emojis ou bullet points.
- **Limites**: Defina tamanho máximo da resposta e comportamento para dados insuficientes.

## Configuração de Agentes (AgentExecutor)
1. Determine as tools necessárias (transações, contas, categorias, etc.).
2. Carregue o modelo com `init_chat_model`.
3. Crie o agente com `create_agent(model=model, tools=tools, system_prompt=SYSTEM_PROMPT)`.
4. Execute com `agent.invoke({'input': user_prompt})`.
5. Capture metadados (`usage_metadata`, `latency`) para logging.

## Tratamento de Erros e Logging
- **Erros de Tool**: Permita que `ValueError` seja levantado para identificar problemas de validação.
- **Fallback**: Em erros do agente, utilize `_generate_fallback_analysis` para sintetizar resposta direta.
- **Logging Estruturado**: Use `logger.info('ai.analysis.completed', extra={...})`.
- **Mensagens Limpa**: Nunca registre valores financeiros ou dados sensíveis em texto puro.
- **Tempo e Tokens**: Registre `elapsed_ms`, `input_tokens`, `output_tokens` para métricas.

## Uso do MCP Context7 para Docs LangChain
1. `mcp__context7__resolve-library-id` com o termo `LangChain`.
2. `mcp__context7__get-library-docs` para tópicos específicos (`agents`, `tools`, `callbacks`).
3. Use `topic` para limitar seções e economizar tokens.
4. Sempre consulte a documentação oficial antes de integrar nova funcionalidade.

## Boas Práticas de Segurança
- Armazene `OPENAI_API_KEY` em `.env` (nunca no código).
- Cumpra LGPD: não exponha dados de terceiros, ofereça transparência e possibilidade de exclusão.
- Limite uma análise por 24h por usuário.
- Garantia de que prompts não exponham dados sensíveis.
- Adicione disclaimers na UI informando que a análise é automatizada.

## Testes e Validação de Agentes
- **Tests**: Cubra isolamento de dados (`ai/tests.py`) e validações de `user_id`.
- **Ambientes**: Execute `python manage.py run_finance_analysis --user-email ...` em staging antes de produção.
- **Observabilidade**: Monitore logs estruturados e tempos de resposta.
- **Fallback**: Teste cenários sem dados (0 transações) e interrupções da OpenAI.
- **Checklist**:
  - Tools obedecem isolamento?
  - Logs estão limpos?
  - UI mostra disclaimers?
  - Documentação atualizada?

## Exemplos de Código
```python
from ai.tools.database_tools import get_user_transactions

# Invocando tool diretamente
transactions = get_user_transactions.invoke({'user_id': 42})

# Configurando agente
agent = initialize_agent(user_id=42)
response = agent.invoke({'input': 'Analise os dados do usuario atual.'})

# Pipeline via serviço
from ai.services.analysis_service import generate_analysis_for_user
analysis = generate_analysis_for_user(42)
print(analysis.analysis_text)
```

---

> **Dica**: Antes de promover mudanças em produção, sincronize com Product Owner e Segurança para validar prompts, políticas de privacidade e experiência do usuário. A IA é uma camada de valor, mas deve operar sempre com transparência e responsabilidade.
