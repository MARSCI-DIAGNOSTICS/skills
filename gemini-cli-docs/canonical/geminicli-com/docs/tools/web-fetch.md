---
source_url: http://geminicli.com/docs/tools/web-fetch
source_type: llms-txt
content_hash: sha256:d7f0a22a9ffbc5815378dbde1493e05955fcb09acb3a6847e88d101acdfccf3e
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"071a555bbe83b7cd68029420f2c21c7f76561e40becb66fb545f20f650888281"'
last_modified: '2026-03-02T02:03:05Z'
---

# Web fetch tool (`web_fetch`)

The `web_fetch` tool allows the Gemini agent to retrieve and process content
from specific URLs provided in your prompt.

## Technical reference

The agent uses this tool when you include URLs in your prompt and request
specific operations like summarization or extraction.

### Arguments

- `prompt` (string, required): A request containing up to 20 valid URLs
  (starting with `http://` or `https://`) and instructions on how to process
  them.

## Technical behavior

- **Confirmation:** Triggers a confirmation dialog showing the converted URLs.
- **Processing:** Uses the Gemini API's `urlContext` for retrieval.
- **Fallback:** If API access fails, the tool attempts to fetch raw content
  directly from your local machine.
- **Formatting:** Returns a synthesized response with source attribution.

## Use cases

- Summarizing technical articles or blog posts.
- Comparing data between two or more web pages.
- Extracting specific information from a documentation site.

## Next steps

- Follow the [Web tools guide](/docs/cli/tutorials/web-tools) for practical
  usage examples.
- See the [Web search tool reference](/docs/tools/web-search) for general queries.
