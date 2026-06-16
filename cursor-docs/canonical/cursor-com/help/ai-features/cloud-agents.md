---
source_url: https://cursor.com/help/ai-features/cloud-agents
source_type: llms-txt
content_hash: sha256:47f1abb2637c1b2a45b887a79de6d8ceb24452bbef6b4bad211f8639bcf4c6f1
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# Cloud Agents

Cloud Agents run in isolated cloud environments instead of on your local machine.

## What can Cloud Agents do?

Cloud Agents handle coding tasks without you needing to be in the loop. They can build features, fix bugs, write tests, open PRs, and share a video of it working. Each task starts from a fresh clone of your repo.

## How does "Move to Cloud" handle my file state?

"Move to Cloud" does not snapshot your local uncommitted changes. The cloud agent starts from a clean git state on the remote repository. It transfers your conversation history and context, but not dirty files or uncommitted edits. Commit or stash your changes before moving a conversation to the cloud if you want the agent to work from your latest state.

## Can Cloud Agents test my app in a browser?

Yes. Each cloud agent runs in its own isolated VM with a full desktop environment. Agents use a mouse and keyboard to control the desktop and browser, the same way a human developer would.

This means agents can start dev servers, open the app in a browser, click through UI flows, and verify their changes work before pushing a PR.

## How do Cloud Agents show their work?

Agents attach screenshots, videos, and log references to the PR so you can validate changes without checking out the branch.

## Can Cloud Agents use MCP tools?

Yes. Add and manage MCP servers through the MCP dropdown at [cursor.com/agents](https://cursor.com/agents). This gives agents access to databases, APIs, and third-party services during their runs.

Cloud agents support HTTP and stdio servers, plus OAuth for servers that need it. See the [Cloud Agent capabilities page](https://cursor.com/docs/cloud-agent/capabilities.md) for setup details.

## Can Cloud Agents fix CI failures?

Yes. Cloud Agents automatically try to fix GitHub Actions failures on PRs they create. They ignore checks that are also failing on the base branch. This is currently available on Teams plans.

To disable this on a specific PR, comment `@cursor autofix off`. To re-enable it, comment `@cursor autofix on`. You can also disable it globally from [Cursor Dashboard > Cloud Agents > My Settings](https://cursor.com/dashboard/cloud-agents).

## What do I need to use Cloud Agents?

You must have a Cursor plan with [on-demand usage](https://cursor.com/docs/account/teams/pricing.md#on-demand-usage) enabled to use cloud agents, which allows you to continue using models after the amount included in your subscription is consumed.

## How do I set up Cloud Agents?

Go to [cursor.com/onboard](https://cursor.com/onboard) to configure your environment. You'll connect your GitHub or GitLab account, select a repository, add any secrets or environment variables, and verify the setup. See the [full setup guide](https://cursor.com/docs/cloud-agent/setup.md) for advanced options like Dockerfiles.

## How do I start a Cloud Agent task?

- **In Cursor**: Select **Cloud** in the dropdown under the agent input
- **On the web**: Go to [cursor.com/agents](https://cursor.com/agents)
- **Via Slack**: Use **@Cursor**
- **On GitHub**: Comment **@cursor** on a PR or issue
- **In Linear**: Use **@Cursor** on an issue
- **Via API**: Use the [Cloud Agent API](https://cursor.com/docs/cloud-agent/api/endpoints.md)

## How is Cloud Agent usage priced?

Cloud Agents are charged at [API pricing](https://cursor.com/docs/models-and-pricing.md#model-pricing) for the selected model. Only Max Mode-compatible models are available.

## Can I run Cloud Agents automatically or on a cron?

Yes. Use [Automations](https://cursor.com/help/ai-features/automations.md) to run Cloud Agents on a schedule or from events in GitHub, Slack, Linear, PagerDuty, or webhooks. Set them up at [cursor.com/automations](https://cursor.com/automations). See the [automations docs](https://cursor.com/docs/cloud-agent/automations.md) for trigger types and templates.

## Does Privacy Mode work with Cloud Agents?

Yes. Cloud Agents are available with Privacy Mode. See the [Cloud Agent security page](https://cursor.com/docs/cloud-agent/security-network.md) for details.

## Related

- [Automations](https://cursor.com/help/ai-features/automations.md)
- [Cloud Agent reference](https://cursor.com/docs/cloud-agent.md)
- [Cloud Agent capabilities](https://cursor.com/docs/cloud-agent/capabilities.md)
- [Cloud Agent setup](https://cursor.com/docs/cloud-agent/setup.md)
- [Automations](https://cursor.com/docs/cloud-agent/automations.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
