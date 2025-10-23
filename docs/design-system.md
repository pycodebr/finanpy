# Design System

Este documento define o sistema de design do Finanpy, incluindo paleta de cores, tipografia, componentes e padrões visuais.

## Visão Geral

O Finanpy utiliza um design moderno com tema escuro e gradientes harmônicos, criando uma experiência visual agradável e profissional. O sistema é construído com TailwindCSS, garantindo responsividade e consistência.

## Paleta de Cores

### Cores Primárias

#### Gradiente Principal
```css
primary-gradient: linear-gradient(135deg, #667eea 0%, #764ba2 100%)
```

Este gradiente é a identidade visual principal do projeto, usado em botões principais, títulos e destaques.

#### Cores Sólidas Primárias
```css
primary-500: #667eea
primary-600: #5568d3
primary-700: #4453bd
```

#### Cores de Accent
```css
accent-500: #764ba2
accent-600: #63418a
accent-700: #503672
```

### Cores de Fundo (Tema Escuro)

```css
bg-primary: #0f172a      /* Fundo principal da página */
bg-secondary: #1e293b    /* Fundo de cards e containers */
bg-tertiary: #334155     /* Fundo de hover e elementos interativos */
```

### Cores de Texto

```css
text-primary: #f1f5f9    /* Texto principal */
text-secondary: #cbd5e1  /* Texto secundário */
text-muted: #64748b      /* Texto menos importante, labels */
```

### Cores de Estado

```css
success: #10b981    /* Verde - entradas, sucesso, confirmações */
error: #ef4444      /* Vermelho - saídas, erros, exclusões */
warning: #f59e0b    /* Amarelo - avisos, atenção */
info: #3b82f6       /* Azul - informações, dicas */
```

### Uso de Cores

- **Transações de Entrada**: Use `success` (verde)
- **Transações de Saída**: Use `error` (vermelho)
- **Botões Primários**: Use gradiente primary-accent
- **Botões Secundários**: Use bg-secondary com borda
- **Botões de Ação Positiva**: Use `success`
- **Botões de Ação Destrutiva**: Use `error`

## Tipografia

### Fonte Principal
```css
font-family: 'Inter', system-ui, -apple-system, sans-serif
```

### Tamanhos de Fonte

| Classe      | Tamanho | Pixels | Uso Recomendado                |
|-------------|---------|--------|--------------------------------|
| text-xs     | 0.75rem | 12px   | Labels pequenas, metadados     |
| text-sm     | 0.875rem| 14px   | Texto secundário, descrições   |
| text-base   | 1rem    | 16px   | Texto padrão do corpo          |
| text-lg     | 1.125rem| 18px   | Subtítulos, destaques          |
| text-xl     | 1.25rem | 20px   | Títulos de cards               |
| text-2xl    | 1.5rem  | 24px   | Títulos de seções              |
| text-3xl    | 1.875rem| 30px   | Títulos principais             |
| text-4xl    | 2.25rem | 36px   | Valores monetários, destaques  |

### Pesos de Fonte

```css
font-normal: 400      /* Texto padrão */
font-medium: 500      /* Destaque leve */
font-semibold: 600    /* Títulos, labels */
font-bold: 700        /* Títulos principais, valores */
```

## Componentes

### Botões

#### Botão Primário
```html
<button class="px-6 py-3 bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-lg font-medium hover:from-primary-600 hover:to-accent-600 transition-all duration-200 shadow-lg hover:shadow-xl">
    Texto do Botão
</button>
```

**Uso**: Ações principais, CTAs, submissão de formulários.

#### Botão Secundário
```html
<button class="px-6 py-3 bg-bg-secondary text-text-primary rounded-lg font-medium hover:bg-bg-tertiary transition-all duration-200 border border-bg-tertiary">
    Texto do Botão
</button>
```

**Uso**: Ações secundárias, cancelar, voltar.

#### Botão de Sucesso
```html
<button class="px-6 py-3 bg-success text-white rounded-lg font-medium hover:bg-green-600 transition-all duration-200">
    Salvar
</button>
```

**Uso**: Salvar, confirmar, adicionar entrada.

#### Botão de Erro
```html
<button class="px-6 py-3 bg-error text-white rounded-lg font-medium hover:bg-red-600 transition-all duration-200">
    Excluir
</button>
```

**Uso**: Deletar, cancelar assinatura, remover.

#### Botão Pequeno
```html
<button class="px-4 py-2 text-sm bg-gradient-to-r from-primary-500 to-accent-500 text-white rounded-md font-medium hover:from-primary-600 hover:to-accent-600 transition-all duration-200">
    Ação
</button>
```

**Uso**: Ações em tabelas, ações rápidas.

### Formulários

#### Input de Texto
```html
<div class="mb-4">
    <label class="block text-text-secondary text-sm font-medium mb-2">
        Label do Campo
    </label>
    <input type="text"
           class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
           placeholder="Digite aqui...">
</div>
```

#### Select
```html
<div class="mb-4">
    <label class="block text-text-secondary text-sm font-medium mb-2">
        Selecione uma opção
    </label>
    <select class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200">
        <option>Opção 1</option>
        <option>Opção 2</option>
    </select>
</div>
```

#### Textarea
```html
<div class="mb-4">
    <label class="block text-text-secondary text-sm font-medium mb-2">
        Descrição
    </label>
    <textarea rows="4"
              class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
              placeholder="Digite aqui..."></textarea>
</div>
```

#### Input Numérico (Valor Monetário)
```html
<div class="mb-4">
    <label class="block text-text-secondary text-sm font-medium mb-2">
        Valor
    </label>
    <input type="number"
           step="0.01"
           class="w-full px-4 py-3 bg-bg-secondary border border-bg-tertiary rounded-lg text-text-primary focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent transition-all duration-200"
           placeholder="0,00">
</div>
```

### Cards

#### Card Padrão
```html
<div class="bg-bg-secondary rounded-xl p-6 shadow-lg border border-bg-tertiary">
    <h3 class="text-xl font-semibold text-text-primary mb-4">Título do Card</h3>
    <p class="text-text-secondary">Conteúdo do card aqui...</p>
</div>
```

**Uso**: Containers gerais, agrupamento de informações.

#### Card com Gradiente
```html
<div class="bg-gradient-to-br from-primary-500 to-accent-500 rounded-xl p-6 shadow-xl">
    <h3 class="text-xl font-semibold text-white mb-2">Saldo Total</h3>
    <p class="text-3xl font-bold text-white">R$ 10.500,00</p>
</div>
```

**Uso**: Destaque de valores principais, métricas importantes.

#### Card de Estatística
```html
<div class="bg-bg-secondary rounded-xl p-6 shadow-lg border border-bg-tertiary hover:border-primary-500 transition-all duration-200">
    <div class="flex items-center justify-between mb-2">
        <span class="text-text-secondary text-sm font-medium">Entradas</span>
        <span class="text-success text-sm">↑</span>
    </div>
    <p class="text-2xl font-bold text-text-primary">R$ 5.200,00</p>
    <p class="text-text-muted text-xs mt-1">+12% vs mês anterior</p>
</div>
```

**Uso**: Dashboard, métricas, KPIs.

### Tabelas

```html
<div class="bg-bg-secondary rounded-xl shadow-lg border border-bg-tertiary overflow-hidden">
    <table class="w-full">
        <thead>
            <tr class="bg-bg-tertiary">
                <th class="px-6 py-4 text-left text-text-secondary text-sm font-semibold">Coluna 1</th>
                <th class="px-6 py-4 text-left text-text-secondary text-sm font-semibold">Coluna 2</th>
                <th class="px-6 py-4 text-left text-text-secondary text-sm font-semibold">Ações</th>
            </tr>
        </thead>
        <tbody>
            <tr class="border-t border-bg-tertiary hover:bg-bg-tertiary transition-all duration-150">
                <td class="px-6 py-4 text-text-primary">Dado 1</td>
                <td class="px-6 py-4 text-text-primary">Dado 2</td>
                <td class="px-6 py-4">
                    <button class="text-primary-500 hover:text-primary-400 text-sm font-medium">Editar</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

**Uso**: Listagem de transações, contas, categorias.

### Navegação

#### Navbar Horizontal
```html
<nav class="bg-bg-secondary border-b border-bg-tertiary shadow-lg">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between h-16">
            <div class="flex items-center">
                <span class="text-2xl font-bold bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">
                    Finanpy
                </span>
            </div>
            <div class="flex items-center space-x-4">
                <a href="#" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Dashboard</a>
                <a href="#" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Contas</a>
                <a href="#" class="text-text-secondary hover:text-text-primary transition-colors duration-200">Transações</a>
                <button class="px-4 py-2 bg-error text-white rounded-lg text-sm font-medium hover:bg-red-600 transition-all duration-200">
                    Sair
                </button>
            </div>
        </div>
    </div>
</nav>
```

#### Sidebar Vertical
```html
<aside class="w-64 bg-bg-secondary h-screen fixed left-0 top-0 border-r border-bg-tertiary p-6">
    <div class="mb-8">
        <span class="text-2xl font-bold bg-gradient-to-r from-primary-500 to-accent-500 bg-clip-text text-transparent">
            Finanpy
        </span>
    </div>
    <nav class="space-y-2">
        <a href="#" class="flex items-center px-4 py-3 text-text-primary bg-bg-tertiary rounded-lg font-medium">
            Dashboard
        </a>
        <a href="#" class="flex items-center px-4 py-3 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-all duration-200">
            Contas
        </a>
        <a href="#" class="flex items-center px-4 py-3 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-all duration-200">
            Categorias
        </a>
        <a href="#" class="flex items-center px-4 py-3 text-text-secondary hover:text-text-primary hover:bg-bg-tertiary rounded-lg transition-all duration-200">
            Transações
        </a>
    </nav>
</aside>
```

### Alertas e Mensagens

#### Mensagem de Sucesso
```html
<div class="bg-success/10 border border-success/20 rounded-lg p-4 mb-4">
    <p class="text-success font-medium">Operação realizada com sucesso!</p>
</div>
```

#### Mensagem de Erro
```html
<div class="bg-error/10 border border-error/20 rounded-lg p-4 mb-4">
    <p class="text-error font-medium">Ocorreu um erro. Tente novamente.</p>
</div>
```

#### Mensagem de Aviso
```html
<div class="bg-warning/10 border border-warning/20 rounded-lg p-4 mb-4">
    <p class="text-warning font-medium">Atenção: verifique os dados informados.</p>
</div>
```

#### Mensagem de Informação
```html
<div class="bg-info/10 border border-info/20 rounded-lg p-4 mb-4">
    <p class="text-info font-medium">Informação importante sobre o sistema.</p>
</div>
```

## Layout e Grid

### Container Principal
```html
<div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <!-- Conteúdo -->
</div>
```

### Grid Responsivo

#### 2 Colunas
```html
<div class="grid grid-cols-1 md:grid-cols-2 gap-6">
    <div>Coluna 1</div>
    <div>Coluna 2</div>
</div>
```

#### 3 Colunas
```html
<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div>Coluna 1</div>
    <div>Coluna 2</div>
    <div>Coluna 3</div>
</div>
```

#### 4 Colunas (Cards de Dashboard)
```html
<div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
    <div>Card 1</div>
    <div>Card 2</div>
    <div>Card 3</div>
    <div>Card 4</div>
</div>
```

## Espaçamentos

### Padding e Margin
```css
spacing-1: 0.25rem   /* 4px */
spacing-2: 0.5rem    /* 8px */
spacing-3: 0.75rem   /* 12px */
spacing-4: 1rem      /* 16px */
spacing-6: 1.5rem    /* 24px */
spacing-8: 2rem      /* 32px */
spacing-12: 3rem     /* 48px */
spacing-16: 4rem     /* 64px */
```

### Bordas Arredondadas
```css
rounded-md: 0.375rem   /* 6px - botões pequenos */
rounded-lg: 0.5rem     /* 8px - botões, inputs */
rounded-xl: 0.75rem    /* 12px - cards */
rounded-2xl: 1rem      /* 16px - containers grandes */
```

### Sombras
```css
shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05)
shadow: 0 1px 3px rgba(0, 0, 0, 0.1)
shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1)
shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1)
shadow-xl: 0 20px 25px rgba(0, 0, 0, 0.15)
```

## Responsividade

### Breakpoints TailwindCSS
```css
sm: 640px    /* Tablets pequenos */
md: 768px    /* Tablets */
lg: 1024px   /* Desktops pequenos */
xl: 1280px   /* Desktops */
2xl: 1536px  /* Desktops grandes */
```

### Padrões Responsivos

- **Mobile-first**: Começar com design mobile e adicionar complexidade
- **Cards**: 1 coluna em mobile, 2-3 em tablet, 3-4 em desktop
- **Tabelas**: Scroll horizontal em mobile ou transformar em cards
- **Sidebar**: Hidden em mobile, visível em desktop
- **Fontes**: Reduzir 1-2 tamanhos em mobile

## Animações e Transições

### Duração Padrão
```css
transition-all duration-200  /* Padrão para hover, focus */
transition-all duration-300  /* Animações mais lentas */
transition-all duration-150  /* Animações rápidas */
```

### Efeitos Comuns
```html
<!-- Hover em Cards -->
<div class="hover:shadow-xl hover:border-primary-500 transition-all duration-200">

<!-- Hover em Botões -->
<button class="hover:from-primary-600 hover:to-accent-600 transition-all duration-200">

<!-- Hover em Links -->
<a class="hover:text-text-primary transition-colors duration-200">
```

## Formatação de Valores Monetários

### Display de Valores
```html
<!-- Valor Grande (Destaque) -->
<p class="text-4xl font-bold text-text-primary">R$ 10.500,00</p>

<!-- Valor Médio -->
<p class="text-2xl font-semibold text-text-primary">R$ 2.350,00</p>

<!-- Valor Pequeno -->
<p class="text-base font-medium text-text-primary">R$ 150,00</p>

<!-- Entrada (Verde) -->
<p class="text-2xl font-bold text-success">+ R$ 5.200,00</p>

<!-- Saída (Vermelho) -->
<p class="text-2xl font-bold text-error">- R$ 3.800,00</p>
```

## Ícones e Símbolos

### Recomendações
- Use ícones SVG quando possível
- Biblioteca sugerida: Heroicons (compatível com Tailwind)
- Tamanho padrão: 20px (w-5 h-5)
- Tamanho pequeno: 16px (w-4 h-4)
- Tamanho grande: 24px (w-6 h-6)

### Símbolos Comuns
- ↑ : Entrada, aumento
- ↓ : Saída, diminuição
- ✓ : Sucesso, confirmado
- ⚠ : Aviso, atenção
- ℹ : Informação

## Acessibilidade

### Contraste
- Texto em fundo escuro: mínimo 4.5:1
- Texto grande (18px+): mínimo 3:1
- Use as cores definidas para garantir contraste adequado

### Focus States
Sempre inclua estados de foco visíveis:
```html
<input class="focus:outline-none focus:ring-2 focus:ring-primary-500">
```

### Labels
Sempre use labels em inputs:
```html
<label for="amount">Valor</label>
<input id="amount" type="number">
```

## Checklist de Design

Ao criar novos componentes, verifique:

- [ ] Usa cores da paleta definida
- [ ] Tem estados de hover e focus
- [ ] É responsivo (mobile, tablet, desktop)
- [ ] Tem espaçamentos consistentes
- [ ] Usa tipografia definida
- [ ] Tem transições suaves
- [ ] Contraste adequado (acessibilidade)
- [ ] Labels e placeholders claros
