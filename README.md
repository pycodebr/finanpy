# Finanpy

Finanpy é um gerenciador de finanças pessoais desenvolvido com Django 5, Python 3.13 e TailwindCSS. A plataforma permite cadastrar contas bancárias, registrar transações, acompanhar métricas no dashboard e, a partir da Sprint 8, gerar análises inteligentes com IA.

## 🚀 Principais Recursos
- Autenticação com usuário customizado (login por e-mail)
- Cadastro de contas, categorias e transações
- Dashboard com visão consolidada (saldo, gráficos, transações recentes)
- Agente de IA financeiro baseado em LangChain + OpenAI (`gpt-4o-mini`)
- Comando Django para gerar análises por usuário ou em lote

## 🛠️ Setup Rápido
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### Variáveis de Ambiente
Copie o template e configure sua chave da OpenAI:
```bash
cp .env.example .env
```
Edite `.env` adicionando:
```env
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxxxxxxxxx
AI_MODEL=gpt-4o-mini
AI_MAX_TOKENS=1000
AI_TEMPERATURE=0.7
```

> **Segurança**: Nunca commit o `.env` ou sua chave da OpenAI.

## 🤖 Gerando Análises com IA
Execute o comando abaixo (usuário deve ter dados financeiros):
```bash
python manage.py run_finance_analysis --user-email usuario@example.com
```
Opcionalmente, processe todos os usuários ativos:
```bash
python manage.py run_finance_analysis --all
```
O sistema respeita limite de 1 análise por usuário a cada 24h, armazena o resultado em `AIAnalysis` e exibe a última análise no dashboard.

## 📄 Documentação
- [Arquitetura](docs/architecture.md)
- [Modelos de Dados](docs/data-models.md)
- [Design System](docs/design-system.md)
- [Documentação do Agente de IA](docs/ai-financial-agent.md)
- [Guia do AI Integration Expert](agents/ai_integration_expert.md)

## ✅ Testes
```bash
python manage.py test
```
Testes específicos do módulo de IA:
```bash
python manage.py test ai.tests
```

## ⚖️ Compliance & Privacidade
- Dados de cada usuário são isolados via filtros `user_id`.
- A IA utiliza exclusivamente os dados do usuário autenticado.
- Logs não armazenam valores financeiros sensíveis.
- A UI inclui disclaimer informando que a análise é automatizada.

## 📬 Suporte
1. Consulte os documentos em `docs/`.
2. Verifique os logs (`ai.services.analysis_service`).
3. Execute tools individualmente no shell (`python manage.py shell`).
4. Em caso de dúvidas sobre IA, acesse `agents/ai_integration_expert.md`.

---

Finanpy é mantido pela equipe interna como projeto de estudo e referência de boas práticas Django + IA. Contribuições são bem-vindas! 🧠💸
