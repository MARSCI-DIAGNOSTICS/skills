---
source_url: https://cursor.com/help/customization/ignore-files
source_type: llms-txt
content_hash: sha256:93720fd8dbcb5fdd324357386d7f9d7bd2cefe89a9a52e91e4d73758b01296ae
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# Ignore files

Control which files Cursor indexes and includes in AI context by using ignore files.

## How do I exclude files from Cursor?

Create a `.cursorignore` file in your project root. Add patterns for files and folders you want excluded:

```text
node_modules/
dist/
*.min.js
.env*
```

Cursor already ignores `.env` files, `.git/`, and lock files by default. See the [full default ignore list](https://cursor.com/docs/reference/ignore-file.md) for details.

Ignored files are blocked from indexing and Agent. Terminal commands and MCP tools run outside of Cursor's file access controls, so they may still be able to read ignored files.

## Does Cursor respect .gitignore?

Yes. Cursor automatically respects your `.gitignore` patterns. Files ignored by git are also ignored by Cursor's indexing.

`.cursorignore` is for additional exclusions beyond what `.gitignore` covers.

## Why should I ignore files?

- **Large generated files** slow down indexing
- **Secrets and credentials** are safer excluded from AI context
- **Binary files and assets** add noise without value
- **Third-party code** (like `node_modules`) is rarely useful as context

## Related

- [Ignore files reference](https://cursor.com/docs/reference/ignore-file.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
