---
name: model-content
description: Design content type schema with fields, validation, and relationships. Use for content modeling workshops or quick schema design.
argument-hint: <content-type-name> [--mode full|quick|guided] [--format yaml|json|csharp]
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Model Content Command

Design a content type schema with parts, fields, and validation rules.

## Usage

```bash
/cms:model-content Article --mode guided
/cms:model-content Product --mode quick --format csharp
/cms:model-content Event --mode full
```

## Modes

- **full**: Complete workshop with stakeholder questions
- **quick**: Fast schema generation with sensible defaults
- **guided**: Interactive step-by-step field definition

## Workflow

### Step 1: Parse Arguments

Extract content type name and options from the command.

### Step 2: Execute Based on Mode

**Full Mode:**

- Invoke `cms-facilitator content-modeling` agent for workshop
- Gather requirements through stakeholder questions
- Generate comprehensive schema with rationale

**Quick Mode:**

- Invoke `content-type-modeling` skill
- Generate schema with common patterns for the content type
- Use industry-standard fields

**Guided Mode:**

- Use AskUserQuestion for field-by-field definition
- Ask about each field's type, validation, and purpose
- Build schema incrementally

### Step 3: Generate Output

Generate content type definition in requested format:

- **yaml**: Human-readable specification
- **json**: API-compatible schema
- **csharp**: EF Core entity model

### Step 4: Validate Schema

- Verify required fields are present
- Check field type consistency
- Validate relationship references
- Ensure naming conventions followed

## Output Example

```yaml
content_type:
  name: Article
  display_name: Article
  description: Blog articles and news posts
  stereotype: Document

  parts:
    - name: TitlePart
      built_in: true
    - name: AutoroutePart
      built_in: true
    - name: ArticlePart
      custom: true

  fields:
    - name: Body
      type: HtmlField
      required: true
      editor: wysiwyg

    - name: Excerpt
      type: TextField
      required: false
      hint: Short summary for listings

    - name: FeaturedImage
      type: MediaField
      required: false
      allowed_types: [image/*]

    - name: Categories
      type: TaxonomyField
      taxonomy: categories
      required: true
      min: 1

    - name: Tags
      type: TaxonomyField
      taxonomy: tags
      required: false

    - name: Author
      type: ContentPickerField
      content_types: [Author]
      required: true

  settings:
    creatable: true
    listable: true
    draftable: true
    versionable: true
```

## Related Skills

- `content-type-modeling` - Content type patterns
- `dynamic-schema-design` - EF Core JSON columns
- `content-relationships` - Field relationships
