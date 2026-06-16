---
source_url: https://cursor.com/docs/agent/prompting
source_type: llms-txt
content_hash: sha256:c6b2f0619df6d6ee13760f89101bb117b2127aa7304fae7e66eaacd96cbc19ac
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# Prompting agents

Direct Agent with text prompts in the chat input. You can attach context, images, and voice, and switch models at any point.

## @ mentions

Type `@` in the chat input to attach specific context to your prompt. Start typing after `@` and Cursor shows matching suggestions.

- **Files**: `@auth.ts` to include a specific file
- **Folders**: `@src/components/` to include an entire folder (type `/` after selecting to navigate deeper)
- **Code symbols**: `@getUserById` to reference a specific function, class, or variable
- **Documentation**: `@Docs` to search indexed documentation, including your own (add via `@Docs > Add new doc`)
- **Past chats**: `@Past Chats` to reference context from a previous conversation

Use @ mentions when you know which files are relevant. If you're not sure which files matter, skip it. Agent finds relevant files through its own search.

Cursor 2.0 removed explicit items like `@Web`, `@Git`, `@Definitions`, `@Linter Errors`, and others from the context menu. Agent now self-gathers this context without manual attachment. For example, ask Agent to review changes on your branch instead of using `@Git`.

## Image input

Attach images to your prompt to provide visual context for UI work, debugging, and design implementation.

- **Drag and drop** an image file into the chat input
- **Paste from clipboard** with Cmd+V, including screenshots

This is useful for implementing design mockups, debugging visual issues, and referencing error messages or stack traces without manual transcription.

## Voice input

Click the microphone icon in the chat input to dictate your prompt instead of typing. Speak naturally, include technical details like file and function names, and review the transcription before sending.

## Changing models

Use the model picker dropdown at the top of the chat input to switch models, or press Cmd / to cycle through models. The change applies to the current conversation going forward. Set a default model in **Cursor Settings > Models**.

- **Faster models** work well for quick edits and routine tasks
- **More capable models** are better for complex reasoning and multi-file refactoring

You can switch models mid-conversation, for example when a faster model handled exploration but you need deeper reasoning for implementation. See [Models & Pricing](https://cursor.com/docs/models-and-pricing.md) for the full list.


---

## Sitemap

[Overview of all docs pages](/llms.txt)
