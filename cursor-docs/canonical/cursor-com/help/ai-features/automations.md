---
source_url: https://cursor.com/help/ai-features/automations
source_type: llms-txt
content_hash: sha256:6becf8ce002de7c9a5cc03bece86e240c26bd401e8658dcbfa663c71699e4902
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# Automations

Automations run [Cloud Agents](https://cursor.com/docs/cloud-agent.md) in the background, triggered by schedules or events from GitHub, Slack, Linear, PagerDuty, and webhooks.

## What can Automations do?

Automations let you run Cloud Agents without manual input. Common uses include:

- Reviewing pull requests when they're opened
- Cleaning up feature flags on a schedule
- Triaging bugs from Slack messages
- Running security scans after CI completes

Browse templates in the [Automations marketplace](https://cursor.com/marketplace/automations) to get started.

## How do I create an automation?

1. Go to [cursor.com/automations/new](https://cursor.com/automations/new) or pick a template from the [marketplace](https://cursor.com/marketplace/automations)
2. Choose a trigger (e.g. every hour, when a PR is opened, or when a Slack message arrives)
3. Write a prompt telling the agent what to do
4. Select the tools the agent can use (Open PR, Comment on PR, Send to Slack, MCP, and more)
5. Save and activate the automation

## Which triggers are available?

| Trigger                    | Fires when                                          |
| -------------------------- | --------------------------------------------------- |
| **Scheduled**              | A recurring schedule or cron expression matches     |
| **GitHub: PR opened**      | A non-draft PR is created or marked ready           |
| **GitHub: PR pushed**      | New commits are pushed to an existing PR            |
| **GitHub: PR merged**      | A PR is merged                                      |
| **GitHub: PR commented**   | Someone comments on a PR                            |
| **GitHub: Push to branch** | Commits are pushed to a specific branch             |
| **GitHub: CI completed**   | A GitHub Check finishes                             |
| **GitHub: Draft opened**   | A draft PR is created                               |
| **Slack: New message**     | A message is sent to a connected public channel     |
| **Slack: Channel created** | A new public channel is created                     |
| **Linear: Issue created**  | A new Linear issue is created                       |
| **Linear: Status changed** | An issue's status changes                           |
| **Linear: End of cycle**   | A Linear cycle completes                            |
| **PagerDuty**              | An incident is triggered, acknowledged, or resolved |
| **Webhook**                | An HTTP POST is sent to the automation's endpoint   |

An automation can have more than one trigger. It runs when any of the triggers fire.

## Which tools can automations use?

- **Open pull request**: The agent writes code and opens a PR
- **Comment on pull request**: Posts review comments, inline code comments, or approvals (requires a PR trigger)
- **Request reviewers**: Assigns reviewers on the triggering PR
- **Send to Slack**: Sends messages to a Slack channel
- **Read Slack channels**: Gives read access to public Slack channels
- **MCP server**: Connects external tools and data sources via [MCP](https://cursor.com/docs/mcp.md)
- **Memories**: Stores and recalls persistent notes across runs as named entries (`MEMORIES.md` by default). Use with caution if your automation handles untrusted input; malicious inputs could write misleading memories that affect future runs.

## How are automations billed?

Automations create Cloud Agent runs. Each run is billed at [API pricing](https://cursor.com/docs/models-and-pricing.md#model-pricing) for the selected model.

## How do I control who can see my automation?

Choose a permission level when creating the automation:

- **Private**: Only you can manage it. Team admins can view and disable it.
- **Team Visible**: Team members can view it. Only you can manage it. Team admins can disable it.
- **Team Owned**: Team members can view it. Only team admins can manage it. Creating a team-owned automation requires team admin access.

## How do I write a good automation prompt?

- Be specific about what the agent should check, change, or produce
- Reference the tools you've enabled
- Include decision rules for different cases (e.g. "if the PR touches migrations, request a review from the database team")
- Set a quality bar for when the agent should act vs. do nothing

Browse the [Automations marketplace](https://cursor.com/marketplace/automations) for examples.

## Related

- [Cloud Agents](https://cursor.com/help/ai-features/cloud-agents.md)
- [Automations reference](https://cursor.com/docs/cloud-agent/automations.md)
- [Cloud Agent setup](https://cursor.com/docs/cloud-agent/setup.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
