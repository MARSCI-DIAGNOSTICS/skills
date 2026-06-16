---
name: create-style-guide
description: Generate comprehensive style guide documentation from theme and design tokens. Outputs to markdown, HTML, or Figma tokens.
argument-hint: "[--format markdown|html|figma-tokens] [--include colors|typography|spacing|all]"
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Create Style Guide Command

Generate comprehensive style guide documentation from design tokens and theme configuration.

## Usage

```bash
/cms:create-style-guide --format markdown
/cms:create-style-guide --format html --include all
/cms:create-style-guide --format figma-tokens
```

## Format Options

- **markdown**: Markdown documentation
- **html**: Interactive HTML style guide
- **figma-tokens**: Figma Tokens plugin format

## Workflow

### Step 1: Parse Arguments

Extract format and include options from command.

### Step 2: Load Design Tokens

Read existing design tokens from:

- Token JSON files
- CSS variable definitions
- Theme configuration

### Step 3: Invoke Skills

Invoke relevant skills:

- `design-token-management` - Token analysis
- `multi-site-theming` - Theme variations

### Step 4: Generate Markdown Style Guide

```markdown
# Design System Style Guide

## Table of Contents

1. [Brand Overview](#brand-overview)
2. [Colors](#colors)
3. [Typography](#typography)
4. [Spacing](#spacing)
5. [Components](#components)
6. [Icons](#icons)
7. [Usage Guidelines](#usage-guidelines)

---

## Brand Overview

### Brand Values
- **Professional**: Clean, trustworthy, reliable
- **Modern**: Contemporary, innovative, forward-thinking
- **Accessible**: Inclusive, clear, easy to use

### Voice & Tone
- Clear and concise
- Friendly but professional
- Action-oriented

---

## Colors

### Primary Colors

| Name | Hex | RGB | CSS Variable |
|------|-----|-----|--------------|
| Brand Primary | #2563eb | rgb(37, 99, 235) | `--color-brand-primary` |
| Brand Dark | #1e40af | rgb(30, 64, 175) | `--color-brand-dark` |
| Brand Light | #93c5fd | rgb(147, 197, 253) | `--color-brand-light` |

### Neutral Colors

| Name | Hex | Usage |
|------|-----|-------|
| Gray 50 | #f9fafb | Backgrounds |
| Gray 100 | #f3f4f6 | Subtle backgrounds |
| Gray 500 | #6b7280 | Secondary text |
| Gray 900 | #111827 | Primary text |

### Semantic Colors

| Name | Color | Usage |
|------|-------|-------|
| Success | #22c55e | Confirmations, positive states |
| Warning | #f59e0b | Cautions, important notices |
| Error | #ef4444 | Errors, destructive actions |
| Info | #3b82f6 | Informational messages |

### Color Usage Guidelines

**Do:**
- Use brand primary for CTAs and key actions
- Use semantic colors consistently for their intended purpose
- Ensure 4.5:1 contrast ratio for text

**Don't:**
- Use brand colors for error states
- Mix semantic colors outside their purpose
- Use low-contrast color combinations

---

## Typography

### Font Families

| Purpose | Font | Fallback |
|---------|------|----------|
| Headings | Inter | system-ui, sans-serif |
| Body | Inter | system-ui, sans-serif |
| Code | JetBrains Mono | monospace |

### Type Scale

| Name | Size | Line Height | Usage |
|------|------|-------------|-------|
| Display | 3.815rem | 1.1 | Hero headlines |
| H1 | 3.052rem | 1.2 | Page titles |
| H2 | 2.441rem | 1.2 | Section titles |
| H3 | 1.953rem | 1.3 | Subsections |
| H4 | 1.563rem | 1.3 | Card titles |
| Body | 1rem | 1.6 | Paragraph text |
| Small | 0.8rem | 1.5 | Captions, labels |

### Text Styles

#### Headings
```html
<h1 class="text-h1">Page Title</h1>
<h2 class="text-h2">Section Title</h2>
<h3 class="text-h3">Subsection</h3>
```

#### Body Text

```html
<p class="text-body">Regular paragraph text</p>
<p class="text-lead">Introductory paragraph with emphasis</p>
<p class="text-small">Caption or helper text</p>
```

---

## Spacing

### Spacing Scale

| Token | Value | Usage |
|-------|-------|-------|
| space-1 | 0.25rem | Tight padding |
| space-2 | 0.5rem | Element padding |
| space-4 | 1rem | Component padding |
| space-8 | 2rem | Section gaps |
| space-16 | 4rem | Large gaps |

### Layout Guidelines

- Use `space-4` for standard component padding
- Use `space-8` between related sections
- Use `space-16` between major page sections

---

## Components

### Buttons

#### Primary Button

```html
<button class="btn btn-primary">Primary Action</button>
```

- Use for main CTA
- One primary button per section

#### Secondary Button

```html
<button class="btn btn-secondary">Secondary Action</button>
```

- Use for alternative actions
- Can pair with primary button

#### Button States

| State | Description |
|-------|-------------|
| Default | Normal resting state |
| Hover | Darkened background |
| Active | Further darkened |
| Disabled | 50% opacity, no pointer |

### Cards

```html
<div class="card">
  <img class="card-image" src="..." alt="...">
  <div class="card-content">
    <h3 class="card-title">Title</h3>
    <p class="card-description">Description</p>
  </div>
</div>
```

### Form Elements

#### Text Input

```html
<label class="label" for="email">Email</label>
<input type="email" id="email" class="input" placeholder="you@example.com">
```

#### Validation States

| State | Border Color | Icon |
|-------|--------------|------|
| Default | Gray 300 | None |
| Focus | Brand Primary | None |
| Error | Error Red | Error icon |
| Success | Success Green | Check icon |

---

## Icons

### Icon System

- **Library**: Lucide Icons
- **Size**: 24px default
- **Stroke**: 2px

### Common Icons

| Icon | Name | Usage |
|------|------|-------|
| ➕ | plus | Add actions |
| ✏️ | edit | Edit actions |
| 🗑️ | trash | Delete actions |
| ✓ | check | Success, complete |
| ✕ | x | Close, cancel |

---

## Usage Guidelines

### Accessibility Checklist

- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Text can scale to 200%
- [ ] Interactive elements have focus states
- [ ] Icons have accessible labels

### Responsive Breakpoints

| Name | Min Width | Usage |
|------|-----------|-------|
| mobile | 0 | Mobile-first base |
| tablet | 768px | Tablet and up |
| desktop | 1024px | Desktop and up |
| wide | 1280px | Large screens |

### Performance Guidelines

- Use system fonts for body text when possible
- Lazy load images below the fold
- Limit custom fonts to 2-3 families

### Step 5: Generate Figma Tokens (if format=figma-tokens)

**Figma Tokens Format:**

```json
{
  "global": {
    "colors": {
      "brand": {
        "primary": {
          "value": "#2563eb",
          "type": "color"
        },
        "secondary": {
          "value": "#93c5fd",
          "type": "color"
        }
      },
      "gray": {
        "50": { "value": "#f9fafb", "type": "color" },
        "100": { "value": "#f3f4f6", "type": "color" },
        "500": { "value": "#6b7280", "type": "color" },
        "900": { "value": "#111827", "type": "color" }
      }
    },
    "typography": {
      "fonts": {
        "heading": { "value": "Inter", "type": "fontFamilies" },
        "body": { "value": "Inter", "type": "fontFamilies" }
      },
      "fontSizes": {
        "xs": { "value": "10", "type": "fontSizes" },
        "sm": { "value": "12", "type": "fontSizes" },
        "base": { "value": "16", "type": "fontSizes" },
        "lg": { "value": "20", "type": "fontSizes" },
        "xl": { "value": "25", "type": "fontSizes" }
      },
      "fontWeights": {
        "normal": { "value": "400", "type": "fontWeights" },
        "medium": { "value": "500", "type": "fontWeights" },
        "bold": { "value": "700", "type": "fontWeights" }
      }
    },
    "spacing": {
      "1": { "value": "4", "type": "spacing" },
      "2": { "value": "8", "type": "spacing" },
      "4": { "value": "16", "type": "spacing" },
      "8": { "value": "32", "type": "spacing" }
    },
    "borderRadius": {
      "sm": { "value": "2", "type": "borderRadius" },
      "md": { "value": "6", "type": "borderRadius" },
      "lg": { "value": "8", "type": "borderRadius" },
      "full": { "value": "9999", "type": "borderRadius" }
    }
  },
  "$themes": [
    {
      "id": "light",
      "name": "Light",
      "selectedTokenSets": {
        "global": "enabled"
      }
    }
  ]
}
```

### Step 6: Generate HTML Style Guide (if format=html)

Interactive HTML output with:

- Live color swatches
- Typography specimens
- Component playground
- Code snippets with copy
- Responsive preview

## Related Skills

- `design-token-management` - Token structure
- `multi-site-theming` - Theme variations
