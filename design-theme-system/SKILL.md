---
name: design-theme-system
description: Design token and theming architecture for multi-site/multi-tenant CMS. Includes CSS variables, Tailwind, and design system integration.
argument-hint: "[--format tokens|css-vars|tailwind|all] [--multi-tenant]"
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Design Theme System Command

Design a comprehensive theming architecture with design tokens and multi-site support.

## Usage

```bash
/cms:design-theme-system --format tokens
/cms:design-theme-system --format css-vars --multi-tenant
/cms:design-theme-system --format tailwind
/cms:design-theme-system --format all
```

## Format Options

- **tokens**: Design token JSON schema
- **css-vars**: CSS custom properties
- **tailwind**: Tailwind CSS configuration
- **all**: Complete theme system

## Workflow

### Step 1: Parse Arguments

Extract format and multi-tenant option from command.

### Step 2: Gather Requirements

Use AskUserQuestion to understand:

- How many sites/tenants need theming?
- What level of customization is needed?
- Are there brand guidelines to follow?
- What frontend frameworks are used?

### Step 3: Invoke Skills

Invoke relevant skills:

- `design-token-management` - Token architecture
- `multi-site-theming` - Multi-tenant patterns

### Step 4: Design Token Schema

**Token Hierarchy:**

```yaml
tokens:
  # Primitive tokens (raw values)
  primitive:
    colors:
      blue:
        50: "#eff6ff"
        100: "#dbeafe"
        500: "#3b82f6"
        600: "#2563eb"
        900: "#1e3a8a"

      gray:
        50: "#f9fafb"
        100: "#f3f4f6"
        500: "#6b7280"
        900: "#111827"

      success: "#22c55e"
      warning: "#f59e0b"
      error: "#ef4444"

    spacing:
      0: "0"
      1: "0.25rem"
      2: "0.5rem"
      4: "1rem"
      8: "2rem"
      16: "4rem"

    typography:
      font_families:
        sans: "Inter, system-ui, sans-serif"
        serif: "Merriweather, Georgia, serif"
        mono: "JetBrains Mono, monospace"

      font_sizes:
        xs: "0.75rem"
        sm: "0.875rem"
        base: "1rem"
        lg: "1.125rem"
        xl: "1.25rem"
        2xl: "1.5rem"
        4xl: "2.25rem"

      font_weights:
        normal: 400
        medium: 500
        semibold: 600
        bold: 700

    radii:
      none: "0"
      sm: "0.125rem"
      md: "0.375rem"
      lg: "0.5rem"
      full: "9999px"

  # Semantic tokens (purpose-driven)
  semantic:
    colors:
      background:
        primary: "{primitive.colors.gray.50}"
        secondary: "{primitive.colors.gray.100}"
        inverse: "{primitive.colors.gray.900}"

      text:
        primary: "{primitive.colors.gray.900}"
        secondary: "{primitive.colors.gray.500}"
        inverse: "{primitive.colors.gray.50}"

      brand:
        primary: "{primitive.colors.blue.600}"
        primary_hover: "{primitive.colors.blue.700}"
        secondary: "{primitive.colors.blue.100}"

      feedback:
        success: "{primitive.colors.success}"
        warning: "{primitive.colors.warning}"
        error: "{primitive.colors.error}"

      border:
        default: "{primitive.colors.gray.200}"
        focus: "{primitive.colors.blue.500}"

    spacing:
      content_padding: "{primitive.spacing.4}"
      section_gap: "{primitive.spacing.8}"
      container_max: "1280px"

    typography:
      body:
        family: "{primitive.typography.font_families.sans}"
        size: "{primitive.typography.font_sizes.base}"
        weight: "{primitive.typography.font_weights.normal}"
        line_height: "1.5"

      heading:
        family: "{primitive.typography.font_families.sans}"
        weight: "{primitive.typography.font_weights.bold}"

  # Component tokens
  component:
    button:
      primary:
        background: "{semantic.colors.brand.primary}"
        text: "{semantic.colors.text.inverse}"
        border_radius: "{primitive.radii.md}"
        padding_x: "{primitive.spacing.4}"
        padding_y: "{primitive.spacing.2}"
        font_weight: "{primitive.typography.font_weights.medium}"

      secondary:
        background: "transparent"
        text: "{semantic.colors.brand.primary}"
        border: "1px solid {semantic.colors.brand.primary}"

    card:
      background: "{semantic.colors.background.primary}"
      border: "1px solid {semantic.colors.border.default}"
      border_radius: "{primitive.radii.lg}"
      padding: "{primitive.spacing.4}"
      shadow: "0 1px 3px rgba(0,0,0,0.1)"

    input:
      background: "{semantic.colors.background.primary}"
      border: "1px solid {semantic.colors.border.default}"
      border_radius: "{primitive.radii.md}"
      padding: "{primitive.spacing.2} {primitive.spacing.4}"
      focus_ring: "0 0 0 2px {semantic.colors.border.focus}"
```

### Step 5: Generate CSS Variables

**CSS Output:**

```css
/* Base theme (light mode) */
:root {
  /* Primitive colors */
  --color-blue-50: #eff6ff;
  --color-blue-500: #3b82f6;
  --color-blue-600: #2563eb;
  --color-gray-50: #f9fafb;
  --color-gray-500: #6b7280;
  --color-gray-900: #111827;

  /* Semantic colors */
  --color-bg-primary: var(--color-gray-50);
  --color-bg-secondary: var(--color-gray-100);
  --color-text-primary: var(--color-gray-900);
  --color-text-secondary: var(--color-gray-500);
  --color-brand-primary: var(--color-blue-600);
  --color-border-default: var(--color-gray-200);

  /* Typography */
  --font-family-sans: 'Inter', system-ui, sans-serif;
  --font-size-base: 1rem;
  --font-weight-normal: 400;
  --font-weight-bold: 700;

  /* Spacing */
  --spacing-1: 0.25rem;
  --spacing-2: 0.5rem;
  --spacing-4: 1rem;
  --spacing-8: 2rem;

  /* Component tokens */
  --button-primary-bg: var(--color-brand-primary);
  --button-primary-text: white;
  --button-radius: var(--radius-md);

  --card-bg: var(--color-bg-primary);
  --card-border: 1px solid var(--color-border-default);
  --card-radius: var(--radius-lg);
}

/* Dark mode */
:root[data-theme="dark"],
.dark {
  --color-bg-primary: var(--color-gray-900);
  --color-bg-secondary: var(--color-gray-800);
  --color-text-primary: var(--color-gray-50);
  --color-text-secondary: var(--color-gray-400);
  --color-border-default: var(--color-gray-700);
}

/* Brand override example */
:root[data-brand="acme"] {
  --color-brand-primary: #ff6b35;
  --color-brand-primary-hover: #e85a2a;
  --font-family-sans: 'Poppins', sans-serif;
}
```

### Step 6: Generate Tailwind Config

**Tailwind Configuration:**

```javascript
// tailwind.config.js
const tokens = require('./tokens.json');

module.exports = {
  content: ['./src/**/*.{html,js,jsx,ts,tsx,razor}'],

  theme: {
    colors: {
      transparent: 'transparent',
      current: 'currentColor',

      // Map CSS variables for runtime theming
      brand: {
        primary: 'var(--color-brand-primary)',
        'primary-hover': 'var(--color-brand-primary-hover)',
        secondary: 'var(--color-brand-secondary)',
      },

      bg: {
        primary: 'var(--color-bg-primary)',
        secondary: 'var(--color-bg-secondary)',
        inverse: 'var(--color-bg-inverse)',
      },

      text: {
        primary: 'var(--color-text-primary)',
        secondary: 'var(--color-text-secondary)',
        inverse: 'var(--color-text-inverse)',
      },

      border: {
        DEFAULT: 'var(--color-border-default)',
        focus: 'var(--color-border-focus)',
      },

      // Static palette for non-themed colors
      ...tokens.primitive.colors,
    },

    fontFamily: {
      sans: 'var(--font-family-sans)',
      serif: 'var(--font-family-serif)',
      mono: 'var(--font-family-mono)',
    },

    extend: {
      spacing: tokens.primitive.spacing,
      borderRadius: tokens.primitive.radii,
    },
  },

  plugins: [
    require('@tailwindcss/forms'),
    require('@tailwindcss/typography'),
  ],
};
```

### Step 7: Multi-Tenant Theme Resolution

**Theme Resolution Service:**

```csharp
public class ThemeService
{
    private readonly ITenantResolver _tenantResolver;
    private readonly IThemeRepository _themeRepository;
    private readonly IMemoryCache _cache;

    public async Task<ThemeConfiguration> GetThemeAsync()
    {
        var tenant = await _tenantResolver.ResolveAsync();
        var cacheKey = $"theme:{tenant.Id}";

        return await _cache.GetOrCreateAsync(cacheKey, async entry =>
        {
            entry.AbsoluteExpirationRelativeToNow = TimeSpan.FromMinutes(5);

            // Load theme hierarchy
            var baseTheme = await _themeRepository.GetBaseThemeAsync();
            var brandTheme = await _themeRepository.GetBrandThemeAsync(tenant.BrandId);
            var siteTheme = await _themeRepository.GetSiteThemeAsync(tenant.SiteId);

            // Merge with precedence: site > brand > base
            return MergeThemes(baseTheme, brandTheme, siteTheme);
        });
    }

    public string GenerateCssVariables(ThemeConfiguration theme)
    {
        var sb = new StringBuilder();
        sb.AppendLine(":root {");

        foreach (var token in theme.FlattenTokens())
        {
            sb.AppendLine($"  --{token.Key}: {token.Value};");
        }

        sb.AppendLine("}");
        return sb.ToString();
    }
}
```

**Theme API Endpoint:**

```csharp
[HttpGet("theme.css")]
[ResponseCache(Duration = 300, VaryByHeader = "Host")]
public async Task<IActionResult> GetThemeCss()
{
    var theme = await _themeService.GetThemeAsync();
    var css = _themeService.GenerateCssVariables(theme);

    return Content(css, "text/css");
}
```

### Step 8: Theme Editor UI

**Theme Customization API:**

```yaml
theme_editor:
  sections:
    - name: Colors
      fields:
        - key: brand_primary
          label: Primary Brand Color
          type: color
          path: semantic.colors.brand.primary

        - key: brand_secondary
          label: Secondary Color
          type: color
          path: semantic.colors.brand.secondary

    - name: Typography
      fields:
        - key: font_family
          label: Primary Font
          type: font_picker
          path: primitive.typography.font_families.sans

        - key: heading_font
          label: Heading Font
          type: font_picker
          path: semantic.typography.heading.family

    - name: Layout
      fields:
        - key: border_radius
          label: Corner Roundness
          type: slider
          min: 0
          max: 24
          path: primitive.radii.md

  preview:
    components: [Button, Card, Input, Typography]
    live_update: true
```

## Related Skills

- `design-token-management` - Token architecture
- `multi-site-theming` - Multi-tenant patterns
