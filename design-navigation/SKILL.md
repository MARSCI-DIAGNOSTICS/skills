---
name: design-navigation
description: Design navigation architecture including menus, breadcrumbs, and mega-menus. Generates structured navigation with accessibility.
argument-hint: "[--type primary|footer|mega|breadcrumb|all] [--format yaml|json|html]"
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Design Navigation Command

Design a comprehensive navigation system with menus, breadcrumbs, and navigation APIs.

## Usage

```bash
/cms:design-navigation --type primary
/cms:design-navigation --type mega --format json
/cms:design-navigation --type all
```

## Navigation Types

- **primary**: Main site navigation
- **footer**: Footer link structure
- **mega**: Multi-column dropdown menus
- **breadcrumb**: Hierarchical path navigation
- **all**: Complete navigation system

## Workflow

### Step 1: Parse Arguments

Extract navigation type and output format from command.

### Step 2: Gather Requirements

Use AskUserQuestion to understand:

- What is the site's primary structure?
- How deep should navigation go?
- Are there mega-menu requirements?
- What mobile patterns should be used?

### Step 3: Invoke Skills

Invoke relevant skills for analysis:

- `navigation-architecture` - Navigation patterns
- `page-structure-design` - Page hierarchy
- `url-routing-patterns` - URL structure

### Step 4: Generate Navigation Design

**Primary Navigation:**

```yaml
navigation:
  name: MainNav
  type: primary
  max_depth: 2

  items:
    - label: Home
      url: /
      icon: home

    - label: Products
      url: /products
      children:
        - label: All Products
          url: /products
        - label: Categories
          url: /products/categories
        - label: New Arrivals
          url: /products/new

    - label: About
      url: /about
      children:
        - label: Our Story
          url: /about/story
        - label: Team
          url: /about/team
        - label: Careers
          url: /about/careers

    - label: Contact
      url: /contact

  settings:
    mobile_breakpoint: 768
    mobile_pattern: hamburger
    sticky: true
    transparent_on_home: true
```

**Mega Menu:**

```yaml
mega_menu:
  name: ProductsMega
  trigger: Products
  layout: columns

  columns:
    - heading: Shop by Category
      items:
        - label: Electronics
          url: /products/electronics
          image: /images/nav/electronics.jpg
        - label: Clothing
          url: /products/clothing
          image: /images/nav/clothing.jpg
        - label: Home & Garden
          url: /products/home-garden

    - heading: Featured
      items:
        - label: Best Sellers
          url: /products/best-sellers
          badge: Popular
        - label: Sale Items
          url: /products/sale
          badge: Up to 50% off

    - heading: Quick Links
      items:
        - label: Gift Cards
          url: /gift-cards
        - label: Store Locator
          url: /stores

  promo:
    title: Summer Sale
    description: Up to 50% off selected items
    image: /images/promo/summer-sale.jpg
    url: /products/sale
    cta: Shop Now
```

**Breadcrumb Configuration:**

```yaml
breadcrumbs:
  separator: /
  show_home: true
  home_label: Home
  show_current: true
  max_length: 5
  truncate_middle: true

  schema:
    enabled: true
    type: BreadcrumbList

  patterns:
    - path: /products/:category/:product
      template:
        - label: Home
          url: /
        - label: Products
          url: /products
        - label: "{category.name}"
          url: /products/{category.slug}
        - label: "{product.name}"
          url: null  # Current page

    - path: /blog/:year/:month/:slug
      template:
        - label: Home
          url: /
        - label: Blog
          url: /blog
        - label: "{year}"
          url: /blog/{year}
        - label: "{post.title}"
          url: null
```

### Step 5: Generate Implementation

Provide EF Core model for navigation:

```csharp
public class NavigationMenu
{
    public Guid Id { get; set; }
    public string Name { get; set; }
    public string Type { get; set; } // primary, footer, mega
    public List<NavigationItem> Items { get; set; }
    public NavigationSettings Settings { get; set; }
}

public class NavigationItem
{
    public Guid Id { get; set; }
    public string Label { get; set; }
    public string Url { get; set; }
    public string Icon { get; set; }
    public string Target { get; set; }
    public int SortOrder { get; set; }
    public Guid? ParentId { get; set; }
    public List<NavigationItem> Children { get; set; }
    public bool IsVisible { get; set; }
    public string[] Roles { get; set; } // Role-based visibility
}

public class NavigationSettings
{
    public int MobileBreakpoint { get; set; }
    public string MobilePattern { get; set; }
    public bool Sticky { get; set; }
    public bool TransparentOnHome { get; set; }
}
```

### Step 6: Generate API Endpoint

```csharp
// GET /api/navigation/{name}
[HttpGet("{name}")]
public async Task<ActionResult<NavigationDto>> GetNavigation(
    string name,
    [FromQuery] string locale = "en")
{
    var navigation = await _navigationService
        .GetByNameAsync(name, locale);

    if (navigation == null)
        return NotFound();

    return Ok(navigation);
}

// Response structure
public class NavigationDto
{
    public string Name { get; set; }
    public string Type { get; set; }
    public List<NavigationItemDto> Items { get; set; }
}

public class NavigationItemDto
{
    public string Label { get; set; }
    public string Url { get; set; }
    public string Icon { get; set; }
    public string Target { get; set; }
    public bool IsActive { get; set; }
    public List<NavigationItemDto> Children { get; set; }
}
```

## Accessibility Requirements

Navigation must meet WCAG 2.1 AA:

| Requirement | Implementation |
|-------------|----------------|
| Keyboard Navigation | Tab order, arrow keys, Enter/Space |
| ARIA Labels | `aria-label`, `aria-expanded`, `aria-current` |
| Focus Management | Visible focus indicators |
| Skip Links | "Skip to main content" link |
| Mobile Touch | Touch target minimum 44x44px |

## Related Skills

- `navigation-architecture` - Navigation patterns
- `page-structure-design` - Page hierarchy
- `url-routing-patterns` - URL patterns
