---
source_url: https://cursor.com/help/ai-features/bugbot
source_type: llms-txt
content_hash: sha256:359852087759f9bda84ff75cda58410accbe91faba8b6eb73a5601396a5b7b18
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# Bugbot

Bugbot reviews your pull requests and catches bugs, security issues, and code quality problems.

## Can Cursor review my PRs?

Yes, Bugbot is Cursor's automated PR review product. It analyzes every pull request for bugs, security vulnerabilities, and code quality issues, leaving inline comments with explanations and suggested fixes.

## What is Bugbot?

Bugbot analyzes PR diffs and leaves comments with explanations and fix suggestions. It runs automatically on each PR update, or you can trigger it manually.

Every user on a Teams or Individual plan gets a limited number of free PR reviews each month. You can upgrade to Bugbot Pro for reviews on up to 200 PRs per month.

## How do I set up Bugbot?

1. Go to [cursor.com/dashboard](https://cursor.com/dashboard/integrations)
2. Navigate to the **Integrations** tab
3. Click **Connect GitHub** (or **Manage Connections** if already connected)
4. Follow the GitHub installation flow
5. Return to the dashboard to enable Bugbot on specific repositories

For GitLab, GitHub Enterprise Server, or self-hosted setups, see the [full setup guide](https://cursor.com/docs/bugbot.md#setup).

## How do I trigger a review?

Bugbot runs automatically when a PR is created or updated. To trigger a review manually, comment `cursor review` or `bugbot run` on any PR.

## How do I customize what Bugbot checks?

Create `.cursor/BUGBOT.md` files in your repository to give Bugbot project-specific review guidelines. Bugbot always includes the root file and traverses upward from changed files to find relevant context.

Team admins can also create organization-wide rules from the [Bugbot dashboard](https://cursor.com/dashboard/bugbot).

## What does Bugbot Pro include?

Bugbot Pro costs $40 per month and covers reviews on up to 200 PRs per month. For teams, the cost is $40 per user per month, and only users who author reviewed PRs count as seats.

See the [full pricing details](https://cursor.com/docs/bugbot.md#pricing).

## How do I fix Bugbot not reviewing my PRs?

1. Comment `cursor review verbose=true` on the PR for detailed logs and a request ID
2. Check that Bugbot has repository access in your [dashboard](https://cursor.com/dashboard/bugbot)
3. Verify the GitHub app is installed and enabled for the repository

Include the request ID from verbose mode when reporting issues to support.

## Related

- [Bugbot reference](https://cursor.com/docs/bugbot.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
