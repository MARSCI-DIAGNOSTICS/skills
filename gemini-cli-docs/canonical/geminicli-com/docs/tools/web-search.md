---
source_url: http://geminicli.com/docs/tools/web-search
source_type: llms-txt
content_hash: sha256:3a016af1e915840dc0a42b876c72ac85109981b013d158f5e2d7b36dc6a89e97
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"b9b2095c85f0aa157d2ec59df923e28e4aab0d3bff5841bbe425571d5dcef907"'
last_modified: '2026-03-02T02:03:05Z'
---

# Web search tool (`google_web_search`)

The `google_web_search` tool allows the Gemini agent to retrieve up-to-date
information, news, and facts from the internet via Google Search.

## Technical reference

The agent uses this tool when your request requires knowledge of current events
or specific online documentation not available in its internal training data.

### Arguments

- `query` (string, required): The search query to be executed.

## Technical behavior

- **Grounding:** Returns a generated summary based on search results.
- **Citations:** Includes source URIs and titles for factual grounding.
- **Processing:** The Gemini API processes the search results before returning a
  synthesized response to the agent.

## Use cases

- Researching the latest version of a software library or API.
- Finding solutions to recent software bugs or security vulnerabilities.
- Retrieving news or documentation updated after the model's knowledge cutoff.

## Next steps

- Follow the [Web tools guide](/docs/cli/tutorials/web-tools) for practical
  usage examples.
- Explore the [Web fetch tool reference](/docs/tools/web-fetch) for direct URL access.
