---
source_url: https://cursor.com/help/customization/context
source_type: llms-txt
content_hash: sha256:a6698b8f16b73f0f5c0ad3c3e4489a6809c1cca967faa5aa14fbdff97011d93c
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# @ mentions and context

Type `@` in the chat input to attach specific context to your conversation. This helps Agent focus on the right files and information.

## What can I reference with @?

- **Files**: `@auth.ts` to include a specific file
- **Folders**: `@src/components/` to include an entire folder
- **Code symbols**: `@getUserById` to reference a specific function, class, or variable
- **Documentation**: `@docs` to let Agent search documentation
- **Web content**: `@web` to let Agent search the web
- **Codebase**: `@codebase` to search across your entire project
- **Past chats**: `@past chats` to reference context from a previous conversation

Start typing after `@` and Cursor shows matching suggestions.

## When should I use @ mentions?

Use them when you know which files are relevant. For example, if you want Agent to update a component and its tests, mention both files.

If you're not sure which files matter, skip the @ mention. Agent finds relevant files through its own search.

## Can I reference multiple files with @?

Yes. Type `@` multiple times to attach several files. Each one gets added to the conversation context.

## Related

- [Rules](https://cursor.com/help/customization/rules.md)
- [Ignore files](https://cursor.com/help/customization/ignore-files.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
