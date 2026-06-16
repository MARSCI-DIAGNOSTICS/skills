---
name: define-typography
description: Define typography scale and text system. Creates modular scales, text styles, and responsive typography.
argument-hint: "[--scale modular|musical|custom] [--base-size 16] [--ratio 1.25]"
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Define Typography Command

Design a comprehensive typography system with scales, styles, and responsive rules.

## Usage

```bash
/cms:define-typography --scale modular --ratio 1.25
/cms:define-typography --scale musical --base-size 18
/cms:define-typography --scale custom
```

## Scale Options

- **modular**: Mathematical scale with consistent ratio
- **musical**: Based on musical intervals (perfect fourth, major third)
- **custom**: User-defined sizes

## Common Ratios

| Name | Ratio | Use Case |
|------|-------|----------|
| Minor Second | 1.067 | Subtle, minimal |
| Major Second | 1.125 | Subtle hierarchy |
| Minor Third | 1.200 | Body-friendly |
| Major Third | 1.250 | Versatile (default) |
| Perfect Fourth | 1.333 | Strong hierarchy |
| Augmented Fourth | 1.414 | Bold, dramatic |
| Perfect Fifth | 1.500 | Very dramatic |
| Golden Ratio | 1.618 | Classic, elegant |

## Workflow

### Step 1: Parse Arguments

Extract scale type, base size, and ratio from command.

### Step 2: Gather Requirements

Use AskUserQuestion to understand:

- What is the primary reading context (blog, app, marketing)?
- What devices are being targeted?
- Are there existing brand fonts to incorporate?
- What is the desired visual personality?

### Step 3: Invoke Skills

Invoke `design-token-management` skill for token generation.

### Step 4: Generate Type Scale

**Modular Scale (1.25 ratio, 16px base):**

```yaml
typography:
  base_size: 16
  ratio: 1.25
  unit: rem

  scale:
    # Calculated: base * ratio^n
    xs:     # 16 / 1.25^2 = 10.24 → 0.64rem
      size: 0.64rem
      line_height: 1.5

    sm:     # 16 / 1.25 = 12.8 → 0.8rem
      size: 0.8rem
      line_height: 1.5

    base:   # 16 = 1rem
      size: 1rem
      line_height: 1.5

    lg:     # 16 * 1.25 = 20 → 1.25rem
      size: 1.25rem
      line_height: 1.4

    xl:     # 16 * 1.25^2 = 25 → 1.563rem
      size: 1.563rem
      line_height: 1.3

    2xl:    # 16 * 1.25^3 = 31.25 → 1.953rem
      size: 1.953rem
      line_height: 1.3

    3xl:    # 16 * 1.25^4 = 39.06 → 2.441rem
      size: 2.441rem
      line_height: 1.2

    4xl:    # 16 * 1.25^5 = 48.83 → 3.052rem
      size: 3.052rem
      line_height: 1.1

    5xl:    # 16 * 1.25^6 = 61.04 → 3.815rem
      size: 3.815rem
      line_height: 1.1
```

### Step 5: Define Text Styles

**Semantic Text Styles:**

```yaml
text_styles:
  # Headings
  display:
    font_family: "{fonts.heading}"
    font_size: "{scale.5xl}"
    font_weight: 800
    line_height: 1.1
    letter_spacing: -0.02em
    text_transform: none
    responsive:
      mobile:
        font_size: "{scale.3xl}"

  h1:
    font_family: "{fonts.heading}"
    font_size: "{scale.4xl}"
    font_weight: 700
    line_height: 1.2
    letter_spacing: -0.02em
    margin_bottom: "{spacing.4}"
    responsive:
      mobile:
        font_size: "{scale.2xl}"

  h2:
    font_family: "{fonts.heading}"
    font_size: "{scale.3xl}"
    font_weight: 700
    line_height: 1.2
    letter_spacing: -0.01em
    margin_bottom: "{spacing.3}"
    responsive:
      mobile:
        font_size: "{scale.xl}"

  h3:
    font_family: "{fonts.heading}"
    font_size: "{scale.2xl}"
    font_weight: 600
    line_height: 1.3
    margin_bottom: "{spacing.2}"

  h4:
    font_family: "{fonts.heading}"
    font_size: "{scale.xl}"
    font_weight: 600
    line_height: 1.3
    margin_bottom: "{spacing.2}"

  h5:
    font_family: "{fonts.heading}"
    font_size: "{scale.lg}"
    font_weight: 600
    line_height: 1.4

  h6:
    font_family: "{fonts.heading}"
    font_size: "{scale.base}"
    font_weight: 600
    line_height: 1.4
    text_transform: uppercase
    letter_spacing: 0.05em

  # Body text
  body:
    font_family: "{fonts.body}"
    font_size: "{scale.base}"
    font_weight: 400
    line_height: 1.6
    color: "{colors.text.primary}"

  body_large:
    font_family: "{fonts.body}"
    font_size: "{scale.lg}"
    font_weight: 400
    line_height: 1.5
    color: "{colors.text.primary}"

  body_small:
    font_family: "{fonts.body}"
    font_size: "{scale.sm}"
    font_weight: 400
    line_height: 1.5
    color: "{colors.text.secondary}"

  # Special text
  lead:
    font_family: "{fonts.body}"
    font_size: "{scale.xl}"
    font_weight: 400
    line_height: 1.5
    color: "{colors.text.secondary}"

  caption:
    font_family: "{fonts.body}"
    font_size: "{scale.xs}"
    font_weight: 400
    line_height: 1.4
    color: "{colors.text.tertiary}"
    text_transform: uppercase
    letter_spacing: 0.05em

  label:
    font_family: "{fonts.body}"
    font_size: "{scale.sm}"
    font_weight: 500
    line_height: 1.4

  code:
    font_family: "{fonts.mono}"
    font_size: 0.875em
    font_weight: 400
    background: "{colors.bg.code}"
    padding: 0.125em 0.25em
    border_radius: "{radii.sm}"

  blockquote:
    font_family: "{fonts.body}"
    font_size: "{scale.lg}"
    font_style: italic
    line_height: 1.6
    border_left: 4px solid "{colors.brand.primary}"
    padding_left: "{spacing.4}"
    margin: "{spacing.6} 0"
```

### Step 6: Generate CSS

**CSS Output:**

```css
/* Typography Scale */
:root {
  --font-size-xs: 0.64rem;
  --font-size-sm: 0.8rem;
  --font-size-base: 1rem;
  --font-size-lg: 1.25rem;
  --font-size-xl: 1.563rem;
  --font-size-2xl: 1.953rem;
  --font-size-3xl: 2.441rem;
  --font-size-4xl: 3.052rem;
  --font-size-5xl: 3.815rem;

  --font-family-heading: 'Inter', system-ui, sans-serif;
  --font-family-body: 'Inter', system-ui, sans-serif;
  --font-family-mono: 'JetBrains Mono', monospace;
}

/* Text Style Classes */
.text-display {
  font-family: var(--font-family-heading);
  font-size: var(--font-size-5xl);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}

.text-h1 {
  font-family: var(--font-family-heading);
  font-size: var(--font-size-4xl);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.02em;
  margin-bottom: 1rem;
}

.text-body {
  font-family: var(--font-family-body);
  font-size: var(--font-size-base);
  font-weight: 400;
  line-height: 1.6;
}

.text-lead {
  font-family: var(--font-family-body);
  font-size: var(--font-size-xl);
  font-weight: 400;
  line-height: 1.5;
  color: var(--color-text-secondary);
}

/* Responsive Typography */
@media (max-width: 768px) {
  .text-display {
    font-size: var(--font-size-3xl);
  }

  .text-h1 {
    font-size: var(--font-size-2xl);
  }
}

/* Prose (long-form content) */
.prose {
  font-family: var(--font-family-body);
  font-size: var(--font-size-lg);
  line-height: 1.7;
  max-width: 65ch;
}

.prose h1, .prose h2, .prose h3, .prose h4 {
  font-family: var(--font-family-heading);
  margin-top: 2em;
  margin-bottom: 0.5em;
}

.prose p {
  margin-bottom: 1.25em;
}

.prose code {
  font-family: var(--font-family-mono);
  font-size: 0.875em;
  background: var(--color-bg-code);
  padding: 0.125em 0.25em;
  border-radius: 0.25rem;
}
```

### Step 7: Font Loading Strategy

**Font Configuration:**

```yaml
fonts:
  strategy: swap  # font-display value

  families:
    - name: Inter
      source: google  # or self-hosted, adobe
      weights: [400, 500, 600, 700, 800]
      styles: [normal, italic]
      subsets: [latin, latin-ext]
      preload: true
      variable: true

    - name: JetBrains Mono
      source: google
      weights: [400, 700]
      styles: [normal]
      subsets: [latin]
      preload: false

  loading:
    preload_critical: true
    preconnect: true
    subset_critical: "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"

  fallbacks:
    sans: "system-ui, -apple-system, sans-serif"
    serif: "Georgia, Times New Roman, serif"
    mono: "Menlo, Monaco, Consolas, monospace"
```

**HTML Head:**

```html
<!-- Preconnect to font sources -->
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

<!-- Preload critical fonts -->
<link rel="preload" href="/fonts/inter-var.woff2" as="font" type="font/woff2" crossorigin>

<!-- Load fonts with display swap -->
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
```

## Accessibility

Typography must meet WCAG requirements:

| Requirement | Guideline |
|-------------|-----------|
| Minimum body size | 16px (1rem) |
| Line height | 1.5 minimum for body text |
| Line length | 45-75 characters optimal |
| Contrast ratio | 4.5:1 for normal text, 3:1 for large |
| Resize support | Text must scale up to 200% |

## Related Skills

- `design-token-management` - Token architecture
- `multi-site-theming` - Theme integration
