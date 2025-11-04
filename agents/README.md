# Agentes de IA - Finanpy

Este diretório contém os agentes especializados de IA para o desenvolvimento do projeto Finanpy. Cada agente representa um papel específico em um time de desenvolvimento de software, com expertise na stack tecnológica do projeto e responsabilidades bem definidas.

## 📋 Índice de Agentes

### 1. [Backend Django Expert](./backend-django-expert.md)
**Função**: Desenvolvedor Backend especializado em Django

**Responsabilidades**:
- Implementar models, views e lógica de negócio
- Criar e aplicar migrações de banco de dados
- Desenvolver APIs e endpoints
- Garantir segurança e isolamento de dados por usuário
- Otimizar queries e performance do backend
- Implementar validações e regras de negócio

**Stack**:
- Python 3.13+
- Django 5+
- Django ORM
- SQLite3
- Django Auth

**Quando usar**:
- Criar ou modificar models Django
- Implementar views (FBV ou CBV)
- Criar formulários e validações
- Configurar URLs e routing
- Implementar signals e automações
- Trabalhar com autenticação e permissões
- Otimizar queries e performance de banco de dados

**MCP Servers utilizados**:
- `context7`: Para consultar documentação oficial do Django

---

### 2. [Frontend Django Templates Expert](./frontend-django-templates-expert.md)
**Função**: Desenvolvedor Frontend especializado em Django Templates e TailwindCSS

**Responsabilidades**:
- Criar templates Django (DTL)
- Implementar interfaces com TailwindCSS
- Garantir responsividade (mobile-first)
- Seguir design system do projeto
- Implementar componentes reutilizáveis
- Garantir acessibilidade e UX

**Stack**:
- Django Template Language (DTL)
- TailwindCSS 3+
- HTML5 Semântico
- CSS3
- JavaScript Vanilla (interações simples)

**Quando usar**:
- Criar ou modificar templates HTML
- Estilizar páginas com TailwindCSS
- Implementar layouts responsivos
- Criar componentes visuais (cards, formulários, botões)
- Trabalhar com design system (cores, tipografia)
- Implementar feedback visual para usuário
- Garantir acessibilidade (labels, aria)

**MCP Servers utilizados**:
- `context7`: Para consultar documentação oficial do TailwindCSS e Django Templates

---

### 3. [QA/Tester Playwright](./qa-tester-playwright.md)
**Função**: Quality Assurance e Tester End-to-End

**Responsabilidades**:
- Executar testes end-to-end com Playwright
- Validar funcionalidades e fluxos de usuário
- Verificar conformidade com design system
- Capturar screenshots para evidências
- Identificar e documentar bugs
- Testar responsividade em diferentes viewports
- Validar isolamento de dados entre usuários
- Verificar cálculos e dados financeiros

**Stack**:
- Playwright MCP Server
- Python 3.13+ (testes Django)
- Django Test Framework
- Conhecimento de UX/UI

**Quando usar**:
- Testar funcionalidades implementadas
- Validar user journeys completos
- Verificar se design está correto
- Testar autenticação e autorização
- Validar formulários e submissões
- Verificar responsividade (mobile/tablet/desktop)
- Testar isolamento de dados entre usuários
- Capturar evidências visuais (screenshots)
- Detectar erros JavaScript no console

**MCP Servers utilizados**:
- `playwright`: Para navegação, interação, screenshots e validação de interface

---

### 4. [Product Owner](./product-owner.md)
**Função**: Dono do Produto e Gestor de Requisitos

**Responsabilidades**:
- Gerenciar e priorizar requisitos do PRD
- Validar implementações contra critérios de aceitação
- Escrever user stories e critérios de aceitação
- Tomar decisões de produto
- Validar fluxos de usuário
- Garantir alinhamento com visão do produto
- Priorizar features e roadmap

**Conhecimento**:
- PRD completo do Finanpy
- Requisitos funcionais (RF001-RF041)
- User journeys e personas
- Objetivos de negócio e usuário
- Princípios do produto (simplicidade, eficiência)

**Quando usar**:
- Validar se implementação atende requisitos
- Escrever user stories para novas features
- Priorizar features (P0, P1, P2, P3)
- Tomar decisões sobre escopo e funcionalidades
- Resolver ambiguidades em requisitos
- Aprovar ou rejeitar entregas
- Definir critérios de aceitação
- Planejar MVPs e releases

**MCP Servers utilizados**:
- Nenhum (foco em gestão de produto)

---

### 5. [Code Reviewer](./code-reviewer.md)
**Função**: Revisor de Código e Guardião da Qualidade Técnica

**Responsabilidades**:
- Revisar qualidade de código
- Garantir aderência aos padrões do projeto
- Identificar problemas de segurança
- Verificar performance e otimizações
- Sugerir melhorias e refatorações
- Validar testabilidade do código
- Garantir consistência arquitetural

**Áreas de foco**:
- Segurança (isolamento de dados, autenticação)
- Performance (N+1 queries, otimizações)
- Padrões de código (CLAUDE.md)
- Arquitetura e relacionamentos
- Testabilidade e edge cases
- UX/UI (acessibilidade, responsividade)

**Quando usar**:
- Revisar código antes de merge/deploy
- Validar pull requests
- Identificar vulnerabilidades de segurança
- Sugerir otimizações de performance
- Garantir que padrões do projeto são seguidos
- Revisar mudanças em models ou views críticas
- Validar código de novos desenvolvedores

**MCP Servers utilizados**:
- `context7`: Para validar uso correto de APIs Django e boas práticas

---

## 🎯 Fluxo de Trabalho Sugerido

### Implementação de Nova Feature

1. **Product Owner** escreve user story com critérios de aceitação
2. **Backend Django Expert** implementa models, views e lógica de negócio
3. **Frontend Django Templates Expert** cria templates e estilização
4. **Code Reviewer** revisa código (segurança, performance, padrões)
5. **QA/Tester Playwright** testa funcionalidade end-to-end
6. **Product Owner** valida contra critérios de aceitação e aprova

### Correção de Bug

1. **QA/Tester Playwright** identifica e documenta bug com evidências
2. **Product Owner** prioriza bug (crítico, alto, médio, baixo)
3. **Backend/Frontend Expert** corrige bug conforme natureza
4. **Code Reviewer** revisa correção
5. **QA/Tester Playwright** valida que bug foi corrigido
6. **Product Owner** aprova correção

### Refatoração de Código

1. **Code Reviewer** identifica código que precisa refatoração
2. **Product Owner** prioriza refatoração vs novas features
3. **Backend/Frontend Expert** implementa refatoração
4. **Code Reviewer** valida que melhorias foram aplicadas
5. **QA/Tester Playwright** valida que funcionalidade não quebrou
6. **Product Owner** aprova refatoração

## 🔧 Stack Tecnológica do Projeto

### Backend
- **Python 3.13+**
- **Django 5+**
- **SQLite3**
- **Django Auth** (autenticação nativa)

### Frontend
- **Django Template Language (DTL)**
- **TailwindCSS 3+**
- **HTML5 Semântico**
- **JavaScript Vanilla** (mínimo necessário)

### Testing
- **Playwright** (end-to-end tests)
- **Django Test Framework** (unit/integration tests)

### Infraestrutura
- **Git** (controle de versão)
- **GitHub** (repositório)

## 📚 Documentação de Referência

Todos os agentes têm acesso e devem consultar:

- **[PRD.md](../PRD.md)**: Product Requirements Document completo
- **[CLAUDE.md](../CLAUDE.md)**: Padrões de código e convenções obrigatórias
- **[docs/architecture.md](../docs/architecture.md)**: Arquitetura do projeto
- **[docs/coding-standards.md](../docs/coding-standards.md)**: Padrões de código detalhados
- **[docs/design-system.md](../docs/design-system.md)**: Design system (cores, componentes, tipografia)
- **[docs/data-models.md](../docs/data-models.md)**: Estrutura de dados e models

## 🤖 MCP Servers Disponíveis

### Context7
**Propósito**: Consultar documentação oficial atualizada de bibliotecas e frameworks

**Usado por**:
- Backend Django Expert (documentação Django)
- Frontend Django Templates Expert (documentação TailwindCSS e Django Templates)
- Code Reviewer (validar boas práticas)

**Como usar**:
```
1. mcp__context7__resolve-library-id: Resolver nome de biblioteca para ID
2. mcp__context7__get-library-docs: Obter documentação específica sobre tópico
```

**Exemplo**:
```
Tarefa: Implementar filtro de data em QuerySet
1. Resolver ID: "Django"
2. Obter docs: topic="QuerySet date filters"
3. Implementar baseado em documentação oficial
```

### Playwright
**Propósito**: Automação de browser para testes end-to-end

**Usado por**:
- QA/Tester Playwright (testes e validações)

**Principais funções**:
- `playwright_navigate`: Navegar para URL
- `playwright_click`: Clicar em elemento
- `playwright_fill`: Preencher input
- `playwright_screenshot`: Capturar screenshot
- `playwright_get_visible_text`: Obter texto visível
- `playwright_console_logs`: Ver logs do console

## 🎨 Design System Quick Reference

### Cores Principais
- **Background**: `slate-900`, `slate-800`, `slate-700`
- **Text**: `slate-100`, `slate-300`, `slate-500`
- **Primary**: Gradiente roxo (`purple-500` → `purple-700`)
- **Income**: `emerald-500` (verde)
- **Expense**: `red-500` (vermelho)

### Componentes Base
- **Card**: `bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-700`
- **Button Primary**: `bg-gradient-to-r from-purple-500 to-purple-700 text-white px-6 py-3 rounded-lg`
- **Input**: `bg-slate-700 border border-slate-600 rounded-lg text-slate-100 px-4 py-3`

## ⚠️ Princípios do Projeto

Todos os agentes devem seguir estes princípios:

1. **Simplicidade**: Evitar over-engineering, manter código simples
2. **Segurança**: Isolamento de dados por usuário é CRÍTICO
3. **Performance**: Otimizar queries, evitar N+1
4. **Consistência**: Seguir padrões do CLAUDE.md rigorosamente
5. **UX First**: Funcionalidades devem ser intuitivas
6. **Mobile-First**: Design responsivo desde o início

## 🚀 Como Usar os Agentes

### No Claude Code

Quando trabalhar no projeto Finanpy, você pode assumir o papel de um agente específico:

```
Exemplo 1:
"Agindo como Backend Django Expert, implemente o model Category com os campos necessários"

Exemplo 2:
"Agindo como QA/Tester Playwright, teste o fluxo de criação de transação"

Exemplo 3:
"Agindo como Code Reviewer, revise o código em accounts/views.py"

Exemplo 4:
"Agindo como Product Owner, valide se a feature de dashboard atende os requisitos RF032-RF037"

Exemplo 5:
"Agindo como Frontend Django Templates Expert, crie o template para listagem de contas"
```

### Múltiplos Agentes

Você também pode solicitar colaboração entre agentes:

```
"Backend Django Expert e Frontend Django Templates Expert, implementem juntos a feature de filtro de transações"

"Product Owner, escreva a user story para feature X. Depois, Backend Django Expert implemente."

"Code Reviewer, revise o código. Depois QA/Tester Playwright teste a funcionalidade."
```

### 6. [AI Integration Expert](./ai_integration_expert.md)
**Função**: Especialista em Integração de IA com LangChain

**Responsabilidades**:
- Criar e configurar agentes LangChain
- Desenvolver LangChain Tools para acesso a dados Django
- Escrever prompts eficazes e context-aware
- Integrar LLMs (OpenAI, Anthropic) com Django
- Garantir segurança e isolamento de dados em análises de IA
- Otimizar performance e custo de uso de APIs
- Documentar padrões de desenvolvimento de agentes

**Stack**:
- LangChain 1.0
- OpenAI API (gpt-4o-mini)
- Django ORM
- Python 3.13+

**Quando usar**:
- Criar novo agente de IA
- Desenvolver tools LangChain para Django
- Refinar prompts de agentes existentes
- Integrar novo modelo de LLM
- Debugar problemas com agentes
- Otimizar custo de tokens da OpenAI
- Garantir segurança em operações de IA
- Consultar documentação LangChain via Context7

**MCP Servers utilizados**:
- `context7`: Para consultar documentação atualizada do LangChain

---

## 📞 Quando Usar Cada Agente

| Tarefa | Agente Recomendado |
|--------|-------------------|
| Criar model Django | Backend Django Expert |
| Implementar view/URL | Backend Django Expert |
| Criar template HTML | Frontend Django Templates Expert |
| Estilizar com TailwindCSS | Frontend Django Templates Expert |
| Testar funcionalidade | QA/Tester Playwright |
| Validar design visual | QA/Tester Playwright |
| Escrever user story | Product Owner |
| Priorizar features | Product Owner |
| Validar requisitos | Product Owner |
| Revisar código | Code Reviewer |
| Otimizar performance | Code Reviewer |
| Validar segurança | Code Reviewer |
| Criar agente LangChain | AI Integration Expert |
| Desenvolver tools de IA | AI Integration Expert |
| Refinar prompts | AI Integration Expert |
| Integrar LLM | AI Integration Expert |

## 🎓 Especialização vs Colaboração

### Especialização
Cada agente é expert em sua área e deve ser consultado para tarefas específicas de sua competência.

### Colaboração
Muitas tarefas requerem múltiplos agentes trabalhando juntos:
- Backend + Frontend = Feature completa
- Backend/Frontend + Code Reviewer = Código de qualidade
- Qualquer implementação + QA = Funcionalidade validada
- Qualquer tarefa + Product Owner = Alinhamento com requisitos

## 📝 Notas Importantes

1. **Todos os agentes** têm acesso à documentação do projeto (PRD, CLAUDE.md, docs/)
2. **Agentes técnicos** (Backend, Frontend) devem usar context7 para consultar docs oficiais
3. **QA/Tester** deve usar Playwright MCP server para automação
4. **Product Owner** é o guardião dos requisitos e visão do produto
5. **Code Reviewer** é o guardião da qualidade técnica e padrões

## 🔄 Versionamento

**Versão**: 1.0
**Data**: Janeiro 2025
**Projeto**: Finanpy
**Stack**: Python 3.13+ | Django 5+ | TailwindCSS 3+

---

Para começar, escolha o agente apropriado para sua tarefa e consulte o arquivo markdown específico para instruções detalhadas.
