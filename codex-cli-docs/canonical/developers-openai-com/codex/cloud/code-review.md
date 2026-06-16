---
source_url: https://developers.openai.com/codex/cloud/code-review
source_type: llms-txt
content_hash: sha256:0d12dc6975efdf89025f5a3618c88dc0da58ff87f26867af7861d13225fb24f2
sitemap_url: https://developers.openai.com/codex/llms.txt
fetch_method: markdown
---

# Code Review

Codex can review code directly in GitHub. This is great for finding bugs and improving code quality.



<YouTubeEmbed
  title="Codex code review walkthrough"
  videoId="HwbSWVg5Ln4"
  class="mx-auto"
/>

## Setup

Before you can use Codex directly inside GitHub, you will need to make sure [Codex cloud](/codex/cloud) is set up.

Afterwards, you can go into the [Codex settings](https://chatgpt.com/codex/settings/code-review) and enable "Code review" on your repository.

![](/images/codex/code-review/code-review-settings.png)

## Usage

After you have enabled Code review on your repository, you can start using it by tagging `@codex` in a comment on a pull request.

To trigger a review by codex you'll have to specifically write `@codex review`.

![](/images/codex/code-review/review-trigger.png)

Afterwards you'll see Codex react to your comment with 👀 acknowledging that it started your task.

Once completed Codex will leave a regular code review in the PR the same way your team would do.

![](/images/codex/code-review/review-example.png)

## Customizing what Codex looks for

Codex automatically searches your repository for `AGENTS.md` files and follows any **Review guidelines** that you include in them. Add a top-level `AGENTS.md` file (or extend an existing one) with a section such as:

```md
## Review guidelines

- Don't log PII.
- Verify that authentication middleware wraps every route.
```

Codex applies the guidance from the closest `AGENTS.md` file to each changed file, so you can place more specific instructions deeper in the tree when particular packages need extra scrutiny. For one-off requests, mention `@codex review for <special instruction>` in your PR comment (for example, `@codex review for security regressions`) and Codex will prioritize that focus area for that review.

On GitHub Codex will only flag P0 and P1 issues. If you want to have Codex for example call out typos in documentation as an issue, you can call out in the `AGENTS.md` file in your `Review guidelines` section that the model should treat typos as P1.

## Giving Codex other tasks

If you mention `@codex` in a comment with anything other than `review` Codex will kick off a [cloud task](/codex/cloud) instead with the context of your pull request.
