---
source_url: https://cursor.com/help/models-and-usage/available-models
source_type: llms-txt
content_hash: sha256:884372e858b75fedd9b2bde957c8f3802cb7807b39cf080570607ac388a13d1a
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# Available models

Cursor supports a range of AI models from multiple providers.

## How do I switch models?

Open the model selector in your chat or agent panel and choose the model you want, or press Cmd + / to cycle through models. Your selection persists across conversations until you change it.

## Which models are available?

Cursor offers its own in-house model (Composer) alongside frontier models from OpenAI, Anthropic, Google, and xAI. The available models depend on your plan. Hobby users have access to a smaller set, while paid plans unlock all models.

See the [models reference](https://cursor.com/docs/models-and-pricing.md) for the complete list, context window sizes, and capabilities.

## Which model should I use?

- **Auto** selects models that balance intelligence, cost, and reliability. Good for everyday tasks.
- **Premium** selects the most capable models for you. Recommended for complex tasks.
- **Composer** is Cursor's in-house model. Fast, capable for most tasks, and built for interactive coding.
- **Claude Opus** and **GPT Codex** handle complex, multi-step tasks well.
- Some users also prefer **Gemini Pro** and **Grok** models.

See the [models reference](https://cursor.com/docs/models-and-pricing.md) for the full list.

## How much does Auto cost?

Auto has fixed token rates regardless of which model Cursor selects behind the scenes:

- **Input + Cache Write**: $1.25 per 1M tokens
- **Output**: $6.00 per 1M tokens
- **Cache Read**: $0.25 per 1M tokens

## How much does Premium cost?

Premium pricing is based on the selected model's API rate. The Cursor team selects Premium models based on internal benchmarks, evaluations, and user feedback on model quality.

Check the [model pricing table](https://cursor.com/docs/models-and-pricing.md#model-pricing) for per-model rates, and your [usage page](https://cursor.com/dashboard/usage) for cost and model selection at the request level.

## How much do models cost?

Each model has its own per-token rate set by the provider (OpenAI, Anthropic, Google, etc.). Cursor charges at these published API rates with no markup. Your model choice directly affects how quickly your included usage budget is consumed.

For the full pricing table, see [model pricing](https://cursor.com/docs/models-and-pricing.md#model-pricing).

## What model am I talking to?

The active model is shown in the model picker at the top of the chat panel. If you selected **Auto**, Cursor picks the model for each request and the specific model used can vary between conversations. You can click the model picker at any time to see or change your selection.

## What models do subagents use?

Built-in subagents (Explore, Bash, Browser) select their model automatically based on the subtask. Custom subagents default to `inherit`, which uses the parent agent's model. You can override this by setting the `model` field in the subagent's YAML frontmatter to `fast` (for speed-optimized tasks) or a specific model ID.

See [subagent model configuration](https://cursor.com/docs/subagents.md#model-configuration) for details.

## What does "model not available" mean?

Some models may not be available in certain regions based on restrictions set by the model providers (not Cursor). When this happens, those models won't appear in Cursor.

Workarounds:

- **Use Auto**: Auto is available in all regions and selects an available model for each request
- **Try other providers**: Some providers may have fewer regional restrictions. Check each provider's supported-regions page for details.
- **Bring Your Own API Key**: If you have an API key from a provider that serves your region, add it in **Cursor Settings** > **Models**. Calls may still fail if the provider blocks your region even with your own key.

See the [regions reference](https://cursor.com/docs/account/regions.md) for provider-specific availability details.

## Related

- [API keys](https://cursor.com/help/models-and-usage/api-keys.md)
- [Usage and limits](https://cursor.com/help/models-and-usage/usage-limits.md)
- [Cursor Token Fee](https://cursor.com/help/models-and-usage/token-fee.md)
- [Models reference](https://cursor.com/docs/models-and-pricing.md)
- [Model pricing](https://cursor.com/docs/models-and-pricing.md#model-pricing)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
