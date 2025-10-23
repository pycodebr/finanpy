# Base Template Guide

## Overview

The `base.html` template is the foundation for all pages in the Finanpy application. It implements the complete Finanpy Design System with TailwindCSS and provides a consistent, responsive layout.

## File Location

`/Users/azambuja/projects/finanpy/templates/base.html`

## Features Implemented

### 1. HTML5 Structure
- Semantic HTML5 with proper DOCTYPE
- Language set to Portuguese (pt-BR)
- Responsive viewport configuration
- SEO-friendly meta tags

### 2. Typography
- **Google Fonts Integration**: Inter font family (weights 300-800)
- Applied globally to body via custom CSS
- Modern, clean sans-serif typeface

### 3. TailwindCSS Integration
- `{% load tailwind_tags %}` for Django-Tailwind integration
- `{% tailwind_css %}` tag loads compiled Tailwind styles
- Custom animation added to Tailwind config: `animate-slide-in-right`

### 4. Finanpy Design System Colors

#### Background Colors
- Primary: `bg-slate-900` (#0f172a)
- Secondary: `bg-slate-800` (#1e293b)
- Tertiary: `bg-slate-700` (#334155)

#### Text Colors
- Primary: `text-slate-100` (#f1f5f9)
- Secondary: `text-slate-300` (#cbd5e1)
- Muted: `text-slate-500` (#64748b)

#### State Colors
- Success/Income: `bg-emerald-500` (#10b981) - green
- Error/Expense: `bg-red-500` (#ef4444) - red
- Warning: `bg-amber-500` (#f59e0b) - yellow
- Info: `bg-blue-500` (#3b82f6) - blue

#### Accent (Primary Gradient)
```css
linear-gradient(135deg, #667eea 0%, #764ba2 100%)
```
Applied via `.gradient-primary` class

### 5. Django Messages System

Fully styled messages with:
- Fixed positioning (top-right corner)
- Color-coded by message type (success, error, warning, info)
- SVG icons for each message type
- Slide-in animation from right
- Auto-dismiss after 5 seconds
- Manual close button
- Responsive design

#### Message Types and Styling

| Type | Background | Text | Icon |
|------|------------|------|------|
| Success | bg-emerald-500 | text-white | Check circle |
| Error | bg-red-500 | text-white | X circle |
| Warning | bg-amber-500 | text-slate-900 | Alert triangle |
| Info | bg-blue-500 | text-white | Info circle |
| Default | bg-slate-700 | text-slate-100 | Chat bubble |

### 6. Template Blocks

#### Available Blocks for Extension

```django
{% block title %}Finanpy - Gestão Financeira Pessoal{% endblock %}
```
- Override to customize page title
- Default: "Finanpy - Gestão Financeira Pessoal"

```django
{% block extra_css %}{% endblock %}
```
- Add page-specific CSS or style tags
- Loaded after TailwindCSS and custom styles

```django
{% block content %}
<!-- Page content goes here -->
{% endblock %}
```
- Main content area
- Wrapped in `<main>` tag with `min-h-screen`

```django
{% block footer %}
<footer class="bg-slate-800 border-t border-slate-700 py-6 mt-auto">
    <div class="container mx-auto px-4 text-center text-slate-400 text-sm">
        <p>&copy; {% now 'Y' %} Finanpy. Todos os direitos reservados.</p>
    </div>
</footer>
{% endblock %}
```
- Footer block (can be overridden or removed)
- Default footer with copyright notice

```django
{% block extra_js %}{% endblock %}
```
- Add page-specific JavaScript
- Loaded at end of body after custom scripts

### 7. Custom CSS Classes

#### `.gradient-primary`
Primary gradient background for buttons and accents
```css
background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
```

#### `.gradient-primary:hover`
Darker gradient on hover
```css
background: linear-gradient(135deg, #5568d3 0%, #65408a 100%);
```

### 8. Custom JavaScript

#### Auto-dismiss Messages
- Messages automatically fade out after 5 seconds
- Smooth slide-out animation
- Automatic removal from DOM after animation

## Usage Examples

### Basic Page Template

```django
{% extends 'base.html' %}

{% block title %}My Page - Finanpy{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    <h1 class="text-3xl font-bold text-slate-100 mb-6">Page Title</h1>
    <div class="bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-700">
        <p class="text-slate-300">Page content here...</p>
    </div>
</div>
{% endblock %}
```

### Page with Custom CSS

```django
{% extends 'base.html' %}

{% block title %}Custom Page - Finanpy{% endblock %}

{% block extra_css %}
<style>
    .custom-class {
        /* Custom styles */
    }
</style>
{% endblock %}

{% block content %}
<!-- Content -->
{% endblock %}
```

### Page with Custom JavaScript

```django
{% extends 'base.html' %}

{% block title %}Interactive Page - Finanpy{% endblock %}

{% block content %}
<!-- Content -->
{% endblock %}

{% block extra_js %}
<script>
    // Custom JavaScript
    console.log('Page loaded');
</script>
{% endblock %}
```

### Page without Footer

```django
{% extends 'base.html' %}

{% block title %}No Footer - Finanpy{% endblock %}

{% block content %}
<!-- Content -->
{% endblock %}

{% block footer %}{% endblock %}
```

## Component Standards

### Primary Button
```html
<button class="px-6 py-3 gradient-primary text-white font-semibold rounded-lg hover:shadow-xl transition-all">
    Button Text
</button>
```

### Secondary Button
```html
<button class="px-6 py-3 bg-slate-700 text-slate-100 font-semibold rounded-lg hover:bg-slate-600 transition-all">
    Button Text
</button>
```

### Card Component
```html
<div class="bg-slate-800 rounded-lg shadow-lg p-6 border border-slate-700">
    <!-- Card content -->
</div>
```

### Input Field
```html
<input type="text" class="w-full px-4 py-3 bg-slate-700 border border-slate-600 rounded-lg text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-purple-500 focus:border-transparent transition-all">
```

## Responsive Breakpoints

Following mobile-first approach:

- **Default**: Mobile layout (< 640px)
- **sm**: Small devices (≥ 640px)
- **md**: Medium devices (≥ 768px)
- **lg**: Large devices (≥ 1024px)
- **xl**: Extra large devices (≥ 1280px)
- **2xl**: 2X large devices (≥ 1536px)

Example:
```html
<div class="text-base md:text-lg lg:text-xl">
    Responsive text size
</div>
```

## Accessibility Features

1. **Semantic HTML**: Proper use of `<header>`, `<main>`, `<footer>`, etc.
2. **Language Attribute**: Set to `pt-BR`
3. **Viewport Meta**: Ensures proper mobile rendering
4. **Focus States**: Visible focus rings on interactive elements
5. **Color Contrast**: Design system ensures WCAG AA compliance
6. **SVG Icons**: Inline SVGs with proper viewBox and stroke properties

## Testing the Template

### Test Home Page
A test home page has been created at `/templates/home.html` that demonstrates:
- Template inheritance from base.html
- Use of design system colors
- Responsive grid layout
- Primary and secondary buttons
- Card components
- Message system testing

### View Test Page
1. Start development server: `python manage.py runserver`
2. Navigate to: `http://127.0.0.1:8000/`
3. Click "Testar Mensagens" to see message system in action

## Tailwind Configuration

Custom animation added to `/theme/static_src/tailwind.config.js`:

```javascript
theme: {
    extend: {
        keyframes: {
            'slide-in-right': {
                '0%': {
                    transform: 'translateX(100%)',
                    opacity: '0',
                },
                '100%': {
                    transform: 'translateX(0)',
                    opacity: '1',
                },
            },
        },
        animation: {
            'slide-in-right': 'slide-in-right 0.3s ease-out',
        },
    },
},
```

## Build Process

After modifying Tailwind config, rebuild CSS:
```bash
cd theme/static_src
npm run build
```

## Related Files

- Base Template: `/templates/base.html`
- Test Home Template: `/templates/home.html`
- Test View: `/core/views.py`
- Tailwind Config: `/theme/static_src/tailwind.config.js`
- Compiled CSS: `/theme/static/css/dist/styles.css`

## Notes

- All templates in the project should extend `base.html`
- Follow the design system colors strictly
- Use TailwindCSS utility classes instead of custom CSS when possible
- Test responsiveness on multiple screen sizes
- Ensure CSRF token is included in all forms (handled by Django)
- Use `{% url %}` tag for all internal links
