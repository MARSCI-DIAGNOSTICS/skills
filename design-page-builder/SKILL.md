---
name: design-page-builder
description: Design a modular page composition system with components, slots, and layout zones. Supports block-based editing.
argument-hint: "[--pattern components|slots|hybrid] [--framework blazor|react|vue]"
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Design Page Builder Command

Design a modular page composition system for block-based content editing.

## Usage

```bash
/cms:design-page-builder --pattern components
/cms:design-page-builder --pattern slots --framework blazor
/cms:design-page-builder --pattern hybrid
```

## Composition Patterns

- **components**: Reusable component library
- **slots**: Named slot-based layouts
- **hybrid**: Components within slot-based templates

## Workflow

### Step 1: Parse Arguments

Extract pattern type and framework from command.

### Step 2: Gather Requirements

Use AskUserQuestion to understand:

- What level of flexibility do editors need?
- Are there specific layout requirements?
- Should components be nestable?
- What preview capabilities are needed?

### Step 3: Invoke Skills

Invoke relevant skills:

- `page-structure-design` - Page templates
- `content-type-modeling` - Component content types

### Step 4: Design Component Library

**Component Definitions:**

```yaml
components:
  # Layout Components
  - name: Section
    category: Layout
    description: Full-width section with background options
    props:
      background_color: string
      background_image: MediaField
      padding: enum[none, small, medium, large]
      width: enum[full, contained, narrow]
    slots:
      - name: content
        allowed: [Hero, Grid, TextBlock, ImageGallery]

  - name: Grid
    category: Layout
    description: Responsive grid container
    props:
      columns: enum[2, 3, 4]
      gap: enum[small, medium, large]
      mobile_stack: boolean
    slots:
      - name: items
        allowed: [Card, Feature, Testimonial]
        min: 1
        max: 12

  # Content Components
  - name: Hero
    category: Content
    description: Hero banner with headline and CTA
    props:
      headline: TextField
      subheadline: TextField
      background_image: MediaField
      background_video: MediaField
      overlay_opacity: number
      text_alignment: enum[left, center, right]
      height: enum[small, medium, large, full]
    slots:
      - name: cta
        allowed: [Button, ButtonGroup]
        max: 1

  - name: TextBlock
    category: Content
    description: Rich text content block
    props:
      content: HtmlField
      alignment: enum[left, center, right, justify]

  - name: Card
    category: Content
    description: Content card with image and text
    props:
      image: MediaField
      title: TextField
      description: TextField
      link: LinkField

  - name: ImageGallery
    category: Media
    description: Responsive image gallery
    props:
      images: MediaField[]
      layout: enum[grid, masonry, carousel]
      columns: number
      lightbox: boolean

  - name: Testimonial
    category: Social Proof
    description: Customer testimonial
    props:
      quote: TextField
      author: TextField
      role: TextField
      avatar: MediaField
      rating: number

  - name: CallToAction
    category: Conversion
    description: CTA section with form or button
    props:
      headline: TextField
      description: TextField
      button_text: TextField
      button_url: LinkField
      form: ContentPickerField[Form]
```

### Step 5: Design Page Templates

**Template with Slots:**

```yaml
templates:
  - name: Homepage
    description: Main landing page template
    slots:
      - name: hero
        label: Hero Section
        allowed: [Hero]
        required: true

      - name: featured
        label: Featured Content
        allowed: [Section, Grid]
        max: 3

      - name: main
        label: Main Content
        allowed: [Section, TextBlock, ImageGallery, Grid]

      - name: testimonials
        label: Testimonials
        allowed: [Testimonial, Grid]

      - name: cta
        label: Call to Action
        allowed: [CallToAction]

  - name: ProductLanding
    description: Product landing page
    slots:
      - name: hero
        allowed: [Hero]
        required: true

      - name: features
        allowed: [Grid, Section]

      - name: pricing
        allowed: [PricingTable]

      - name: faq
        allowed: [Accordion]

      - name: cta
        allowed: [CallToAction]

  - name: BlogPost
    description: Blog article template
    slots:
      - name: header
        allowed: [ArticleHeader]
        required: true

      - name: content
        allowed: [TextBlock, ImageGallery, CodeBlock, Quote]

      - name: author
        allowed: [AuthorBio]

      - name: related
        allowed: [RelatedPosts]
```

### Step 6: Generate Data Model

**EF Core Models:**

```csharp
public class Page
{
    public Guid Id { get; set; }
    public string Title { get; set; }
    public string Slug { get; set; }
    public string TemplateId { get; set; }
    public PageStatus Status { get; set; }

    // JSON column for flexible content
    public PageContent Content { get; set; }
}

[Owned]
public class PageContent
{
    public Dictionary<string, List<ComponentInstance>> Slots { get; set; }
}

[Owned]
public class ComponentInstance
{
    public string Id { get; set; }
    public string ComponentType { get; set; }
    public Dictionary<string, object> Props { get; set; }
    public Dictionary<string, List<ComponentInstance>> NestedSlots { get; set; }
}

// DbContext configuration
modelBuilder.Entity<Page>()
    .OwnsOne(p => p.Content, cb =>
    {
        cb.ToJson();
    });
```

### Step 7: Generate Blazor Components (if framework=blazor)

**Component Renderer:**

```csharp
@* ComponentRenderer.razor *@
@inject IComponentRegistry Registry

@foreach (var component in Components)
{
    <DynamicComponent
        Type="@Registry.GetComponentType(component.ComponentType)"
        Parameters="@GetParameters(component)" />
}

@code {
    [Parameter] public List<ComponentInstance> Components { get; set; }

    private Dictionary<string, object> GetParameters(ComponentInstance instance)
    {
        var parameters = new Dictionary<string, object>(instance.Props);

        if (instance.NestedSlots?.Any() == true)
        {
            parameters["NestedSlots"] = instance.NestedSlots;
        }

        return parameters;
    }
}
```

**Hero Component:**

```csharp
@* Components/Hero.razor *@
<section class="hero @HeightClass" style="@BackgroundStyle">
    @if (OverlayOpacity > 0)
    {
        <div class="hero-overlay" style="opacity: @OverlayOpacity"></div>
    }

    <div class="hero-content @AlignmentClass">
        <h1>@Headline</h1>
        @if (!string.IsNullOrEmpty(Subheadline))
        {
            <p class="hero-subheadline">@Subheadline</p>
        }

        @if (NestedSlots?.ContainsKey("cta") == true)
        {
            <div class="hero-cta">
                <ComponentRenderer Components="@NestedSlots["cta"]" />
            </div>
        }
    </div>
</section>

@code {
    [Parameter] public string Headline { get; set; }
    [Parameter] public string Subheadline { get; set; }
    [Parameter] public string BackgroundImage { get; set; }
    [Parameter] public decimal OverlayOpacity { get; set; }
    [Parameter] public string TextAlignment { get; set; } = "center";
    [Parameter] public string Height { get; set; } = "medium";
    [Parameter] public Dictionary<string, List<ComponentInstance>> NestedSlots { get; set; }

    private string HeightClass => $"hero--{Height}";
    private string AlignmentClass => $"text-{TextAlignment}";
    private string BackgroundStyle =>
        !string.IsNullOrEmpty(BackgroundImage)
            ? $"background-image: url({BackgroundImage})"
            : "";
}
```

## Editor Experience

Design the page builder editor:

```yaml
editor:
  features:
    - drag_drop: true
    - inline_editing: true
    - live_preview: true
    - responsive_preview: [mobile, tablet, desktop]
    - undo_redo: true
    - component_search: true
    - keyboard_shortcuts: true

  sidebar:
    - components_panel
    - settings_panel
    - layers_panel

  toolbar:
    - save
    - preview
    - publish
    - device_toggle
    - undo
    - redo
```

## Related Skills

- `page-structure-design` - Page templates
- `content-type-modeling` - Component types
- `dynamic-schema-design` - JSON column storage
