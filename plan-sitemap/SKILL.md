---
name: plan-sitemap
description: Generate sitemap and URL routing strategy. Creates XML sitemaps, URL patterns, and redirect rules.
argument-hint: "[--output xml|json|tree|yaml] [--include-redirects] [--priority-rules]"
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Plan Sitemap Command

Generate a comprehensive sitemap and URL routing strategy for the CMS.

## Usage

```bash
/cms:plan-sitemap --output xml
/cms:plan-sitemap --output tree --include-redirects
/cms:plan-sitemap --output yaml --priority-rules
```

## Output Formats

- **xml**: Standard XML sitemap (sitemap.xml)
- **json**: JSON sitemap for APIs
- **tree**: Visual ASCII tree structure
- **yaml**: Structured configuration

## Workflow

### Step 1: Parse Arguments

Extract output format and options from command.

### Step 2: Analyze Site Structure

Read existing content types and page definitions:

- Content types with routes
- Page hierarchies
- Taxonomy structures
- Dynamic route patterns

### Step 3: Invoke Skills

Invoke relevant skills:

- `url-routing-patterns` - URL conventions
- `page-structure-design` - Page hierarchy
- `navigation-architecture` - Navigation structure

### Step 4: Generate URL Strategy

**URL Pattern Rules:**

```yaml
url_patterns:
  # Static pages
  static:
    home: /
    about: /about
    contact: /contact
    privacy: /privacy-policy
    terms: /terms-of-service

  # Content types
  content_types:
    Article:
      pattern: /blog/{year}/{month}/{slug}
      example: /blog/2025/01/getting-started

    Product:
      pattern: /products/{category}/{slug}
      example: /products/electronics/wireless-headphones

    Category:
      pattern: /products/{slug}
      example: /products/electronics

    Author:
      pattern: /authors/{slug}
      example: /authors/jane-smith

    Page:
      pattern: /{*slug}  # Catch-all for CMS pages
      example: /about/team/leadership

  # Taxonomies
  taxonomies:
    tags:
      pattern: /tags/{slug}
      example: /tags/technology

    categories:
      pattern: /categories/{slug}
      example: /categories/news

  # Localization
  localization:
    enabled: true
    pattern: /{locale}/{path}
    default_locale: en
    supported: [en, es, fr, de]

  # API routes (excluded from sitemap)
  api:
    pattern: /api/{version}/{resource}
    exclude_from_sitemap: true
```

### Step 5: Generate Sitemap

**XML Sitemap:**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">

  <!-- Homepage -->
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2025-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
    <xhtml:link rel="alternate" hreflang="en" href="https://example.com/" />
    <xhtml:link rel="alternate" hreflang="es" href="https://example.com/es/" />
  </url>

  <!-- Blog posts -->
  <url>
    <loc>https://example.com/blog/2025/01/getting-started</loc>
    <lastmod>2025-01-15</lastmod>
    <changefreq>monthly</changefreq>
    <priority>0.8</priority>
    <image:image>
      <image:loc>https://cdn.example.com/images/getting-started.jpg</image:loc>
      <image:title>Getting Started Guide</image:title>
    </image:image>
  </url>

  <!-- Products -->
  <url>
    <loc>https://example.com/products/electronics/wireless-headphones</loc>
    <lastmod>2025-01-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.9</priority>
  </url>

</urlset>
```

**Sitemap Index (for large sites):**

```xml
<?xml version="1.0" encoding="UTF-8"?>
<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <sitemap>
    <loc>https://example.com/sitemaps/pages.xml</loc>
    <lastmod>2025-01-15</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemaps/products.xml</loc>
    <lastmod>2025-01-14</lastmod>
  </sitemap>
  <sitemap>
    <loc>https://example.com/sitemaps/blog.xml</loc>
    <lastmod>2025-01-15</lastmod>
  </sitemap>
</sitemapindex>
```

**Tree Output:**

```text
SITEMAP STRUCTURE
=================

/ (Home)
├── /about
│   ├── /about/team
│   ├── /about/careers
│   └── /about/press
├── /products
│   ├── /products/electronics
│   │   ├── /products/electronics/headphones
│   │   └── /products/electronics/speakers
│   └── /products/clothing
├── /blog
│   ├── /blog/2025/01/...
│   └── /blog/2024/12/...
├── /contact
├── /privacy-policy
└── /terms-of-service

Legend:
  [S] Static page
  [D] Dynamic content type
  [T] Taxonomy listing
```

### Step 6: Generate Redirect Rules

**Redirect Configuration:**

```yaml
redirects:
  # Permanent redirects (301)
  permanent:
    - from: /old-about
      to: /about

    - from: /blog/{slug}
      to: /blog/2024/01/{slug}
      note: Legacy URL pattern

    - from: /products/{id:int}
      to: /products/legacy/{id}
      note: Numeric ID to slug migration

  # Temporary redirects (302)
  temporary:
    - from: /sale
      to: /products?filter=sale
      expires: 2025-02-28

  # Regex patterns
  patterns:
    - from: ^/category/(.*)$
      to: /categories/$1
      type: 301

  # Trailing slash normalization
  trailing_slash:
    enforce: false  # No trailing slash
    redirect_type: 301

  # Case normalization
  case_sensitivity:
    lowercase: true
    redirect_type: 301
```

### Step 7: Generate Priority Rules

**SEO Priority Configuration:**

```yaml
priority_rules:
  # By content type
  content_types:
    Page:
      default: 0.8
      homepage: 1.0

    Product:
      default: 0.9
      featured: 1.0
      out_of_stock: 0.3

    Article:
      default: 0.7
      featured: 0.9
      age_decay:
        after_days: 90
        minimum: 0.4

  # By depth
  depth:
    - level: 1
      priority: 0.9
    - level: 2
      priority: 0.7
    - level: 3
      priority: 0.5
    - level: 4+
      priority: 0.3

  # Change frequency
  changefreq:
    homepage: daily
    product_listing: daily
    product_detail: weekly
    blog_post: monthly
    static_page: yearly
```

## Implementation

```csharp
public interface ISitemapGenerator
{
    Task<string> GenerateXmlAsync(SitemapOptions options);
    Task<SitemapIndex> GenerateIndexAsync();
    Task<IEnumerable<SitemapUrl>> GetUrlsAsync(ContentType type);
}

public class SitemapUrl
{
    public string Loc { get; set; }
    public DateTime LastMod { get; set; }
    public ChangeFrequency ChangeFreq { get; set; }
    public decimal Priority { get; set; }
    public List<AlternateLink> Alternates { get; set; }
    public List<ImageInfo> Images { get; set; }
}
```

## Related Skills

- `url-routing-patterns` - URL conventions
- `page-structure-design` - Page hierarchy
- `navigation-architecture` - Site structure
