# Finanpy Design System - Quick Reference

## Color Palette

### Backgrounds

| Name | Tailwind Class | Hex Code | RGB | Usage |
|------|---------------|----------|-----|-------|
| Primary | `bg-slate-900` | #0f172a | rgb(15, 23, 42) | Main background, body |
| Secondary | `bg-slate-800` | #1e293b | rgb(30, 41, 59) | Cards, panels, secondary surfaces |
| Tertiary | `bg-slate-700` | #334155 | rgb(51, 65, 85) | Buttons, inputs, tertiary surfaces |

### Text Colors

| Name | Tailwind Class | Hex Code | RGB | Usage |
|------|---------------|----------|-----|-------|
| Primary | `text-slate-100` | #f1f5f9 | rgb(241, 245, 249) | Primary text, headings |
| Secondary | `text-slate-300` | #cbd5e1 | rgb(203, 213, 225) | Secondary text, descriptions |
| Muted | `text-slate-500` | #64748b | rgb(100, 116, 139) | Muted text, placeholders |

### State Colors

| State | Tailwind Class | Hex Code | RGB | Usage |
|-------|---------------|----------|-----|-------|
| Success/Income | `bg-emerald-500` / `text-emerald-500` | #10b981 | rgb(16, 185, 129) | Success messages, income transactions |
| Error/Expense | `bg-red-500` / `text-red-500` | #ef4444 | rgb(239, 68, 68) | Error messages, expense transactions |
| Warning | `bg-amber-500` / `text-amber-500` | #f59e0b | rgb(245, 158, 11) | Warning messages, alerts |
| Info | `bg-blue-500` / `text-blue-500` | #3b82f6 | rgb(59, 130, 246) | Info messages, notifications |

### Accent Colors (Purple Gradient)

| Type | CSS | Usage |
|------|-----|-------|
| Primary Gradient | `linear-gradient(135deg, #667eea 0%, #764ba2 100%)` | Primary buttons, CTAs, accents |
| Hover Gradient | `linear-gradient(135deg, #5568d3 0%, #65408a 100%)` | Hover state for primary buttons |

**Tailwind Classes**: Use custom class `.gradient-primary`

```html
<!-- Primary Button with Gradient -->
<button class="gradient-primary px-6 py-3 text-white rounded-lg">
    Click Me
</button>
```

### Border Colors

| Name | Tailwind Class | Hex Code | Usage |
|------|---------------|----------|-------|
| Default | `border-slate-700` | #334155 | Standard borders on cards |
| Focus | `border-slate-600` | #475569 | Input borders |
| Accent | `border-purple-500` | #a855f7 | Hover borders, active states |

## Typography

### Font Family
- **Primary**: Inter (Google Fonts)
- **Weights Available**: 300, 400, 500, 600, 700, 800
- **Fallback**: sans-serif

### Usage
```css
font-family: 'Inter', sans-serif;
```

Applied globally to `<body>` element.

### Text Sizes (Tailwind)

| Size | Tailwind Class | Font Size | Line Height | Usage |
|------|---------------|-----------|-------------|-------|
| XS | `text-xs` | 12px | 16px | Small labels |
| SM | `text-sm` | 14px | 20px | Descriptions, captions |
| Base | `text-base` | 16px | 24px | Body text |
| LG | `text-lg` | 18px | 28px | Emphasized text |
| XL | `text-xl` | 20px | 28px | Small headings |
| 2XL | `text-2xl` | 24px | 32px | Section headings |
| 3XL | `text-3xl` | 30px | 36px | Page headings |
| 4XL | `text-4xl` | 36px | 40px | Hero headings |
| 5XL | `text-5xl` | 48px | 1 | Large hero headings |
| 6XL | `text-6xl` | 60px | 1 | Extra large headings |

## Spacing Scale

Following Tailwind's default spacing (1 unit = 0.25rem = 4px):

| Class | Pixels | Usage |
|-------|--------|-------|
| `p-1` | 4px | Minimal padding |
| `p-2` | 8px | Small padding |
| `p-3` | 12px | Small-medium padding |
| `p-4` | 16px | Standard padding |
| `p-6` | 24px | Medium padding |
| `p-8` | 32px | Large padding |
| `p-12` | 48px | Extra large padding |
| `p-16` | 64px | Section padding |

Replace `p` with:
- `m` for margin
- `px` for horizontal padding
- `py` for vertical padding
- `pt`, `pr`, `pb`, `pl` for specific sides

## Component Templates

### 1. Card Component

```html
<div class="bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-700">
    <!-- Card content -->
</div>
```

**Variations**:
```html
<!-- Hoverable Card -->
<div class="bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-700 hover:border-purple-500 transition-all">

<!-- Income Transaction Card -->
<div class="bg-slate-800 rounded-lg shadow-lg p-6 border-l-4 border-l-emerald-500">

<!-- Expense Transaction Card -->
<div class="bg-slate-800 rounded-lg shadow-lg p-6 border-l-4 border-l-red-500">
```

### 2. Buttons

#### Primary Button
```html
<button class="px-6 py-3 gradient-primary text-white font-semibold rounded-lg hover:shadow-xl transition-all transform hover:scale-105">
    Primary Action
</button>
```

#### Secondary Button
```html
<button class="px-6 py-3 bg-slate-700 text-slate-100 font-semibold rounded-lg hover:bg-slate-600 transition-all">
    Secondary Action
</button>
```

#### Danger Button
```html
<button class="px-6 py-3 bg-red-500 text-white font-semibold rounded-lg hover:bg-red-600 transition-all">
    Delete
</button>
```

#### Success Button
```html
<button class="px-6 py-3 bg-emerald-500 text-white font-semibold rounded-lg hover:bg-emerald-600 transition-all">
    Confirm
</button>
```

### 3. Form Inputs

#### Text Input
```html
<input type="text"
       class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all"
       placeholder="Enter text...">
```

#### Select Dropdown
```html
<select class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all">
    <option>Option 1</option>
    <option>Option 2</option>
</select>
```

#### Textarea
```html
<textarea class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all resize-none"
          rows="4"
          placeholder="Enter description..."></textarea>
```

#### Label
```html
<label class="block text-slate-300 font-semibold mb-2" for="input-id">
    Label Text
</label>
```

### 4. Badges

#### Success Badge
```html
<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-emerald-500 text-white">
    Active
</span>
```

#### Error Badge
```html
<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-red-500 text-white">
    Inactive
</span>
```

#### Info Badge
```html
<span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-blue-500 text-white">
    Pending
</span>
```

### 5. Lists

#### Unordered List
```html
<ul class="space-y-2">
    <li class="flex items-center text-slate-300">
        <svg class="w-5 h-5 mr-2 text-emerald-500" fill="currentColor" viewBox="0 0 20 20">
            <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd"/>
        </svg>
        List item 1
    </li>
</ul>
```

### 6. Empty States

```html
<div class="bg-slate-800 rounded-lg p-8 text-center border border-slate-700">
    <svg class="w-16 h-16 mx-auto text-slate-500 mb-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"></path>
    </svg>
    <h3 class="text-xl font-semibold text-slate-300 mb-2">No Items Found</h3>
    <p class="text-slate-400 mb-4">You haven't created any items yet.</p>
    <a href="#" class="inline-block px-6 py-3 gradient-primary text-white font-semibold rounded-lg">
        Create First Item
    </a>
</div>
```

## Layout Patterns

### Container
```html
<div class="container mx-auto px-4 py-8">
    <!-- Content -->
</div>
```

### Grid (2 columns)
```html
<div class="grid md:grid-cols-2 gap-6">
    <div>Column 1</div>
    <div>Column 2</div>
</div>
```

### Grid (3 columns)
```html
<div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
    <div>Column 1</div>
    <div>Column 2</div>
    <div>Column 3</div>
</div>
```

### Flexbox (centered)
```html
<div class="flex items-center justify-center min-h-screen">
    <!-- Centered content -->
</div>
```

### Flexbox (space between)
```html
<div class="flex items-center justify-between">
    <div>Left</div>
    <div>Right</div>
</div>
```

## Shadows

| Class | Usage |
|-------|-------|
| `shadow` | Standard shadow for cards |
| `shadow-lg` | Large shadow for elevated cards |
| `shadow-xl` | Extra large shadow for hover states |
| `hover:shadow-xl` | Shadow on hover |

## Border Radius

| Class | Pixels | Usage |
|-------|--------|-------|
| `rounded` | 4px | Small radius |
| `rounded-md` | 6px | Medium radius |
| `rounded-lg` | 8px | Large radius (standard for buttons/cards) |
| `rounded-xl` | 12px | Extra large radius |
| `rounded-full` | 9999px | Fully rounded (badges, avatars) |

## Transitions

Standard transition for all interactive elements:
```html
class="transition-all"
```

For specific properties:
```html
class="transition-colors"  <!-- Only color transitions -->
class="transition-transform"  <!-- Only transform transitions -->
class="transition-opacity"  <!-- Only opacity transitions -->
```

## Responsive Breakpoints

| Prefix | Min Width | Device |
|--------|-----------|--------|
| (none) | 0px | Mobile (default) |
| `sm:` | 640px | Small tablets |
| `md:` | 768px | Tablets |
| `lg:` | 1024px | Desktops |
| `xl:` | 1280px | Large desktops |
| `2xl:` | 1536px | Extra large screens |

### Example
```html
<div class="text-base md:text-lg lg:text-xl">
    <!-- Font size increases on larger screens -->
</div>

<div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3">
    <!-- 1 column mobile, 2 tablet, 3 desktop -->
</div>
```

## Icons

Using Heroicons (SVG):

```html
<!-- Example Icon -->
<svg class="w-6 h-6 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
</svg>
```

Icon sizes:
- `w-4 h-4` - Small (16px)
- `w-5 h-5` - Medium (20px)
- `w-6 h-6` - Standard (24px)
- `w-8 h-8` - Large (32px)

## Usage in Django Templates

```django
{% extends 'base.html' %}

{% block title %}Page Title - Finanpy{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <!-- Use design system components -->
    <div class="bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-700">
        <h1 class="text-3xl font-bold text-slate-100 mb-4">Heading</h1>
        <p class="text-slate-300 mb-6">Description text...</p>
        <button class="gradient-primary px-6 py-3 text-white rounded-lg">
            Action
        </button>
    </div>
</div>
{% endblock %}
```

---

**Note**: Always use these exact color classes and component patterns to maintain visual consistency across the Finanpy application.
