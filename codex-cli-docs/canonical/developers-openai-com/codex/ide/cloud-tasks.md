---
source_url: https://developers.openai.com/codex/ide/cloud-tasks
source_type: llms-txt
content_hash: sha256:c323320098217f2a6d37404f1b81ca76228296b6fa3bf378db54ca6f708ecc08
sitemap_url: https://developers.openai.com/codex/llms.txt
fetch_method: markdown
---

# Codex IDE → Cloud tasks

## Delegate to the cloud agent

You can offload bigger jobs to Codex in the cloud, then track progress and review results without leaving your IDE.

First, you'll need to [set up a cloud environment for Codex](https://chatgpt.com/codex/settings/environments) to work in.
Then pick your environment and select `Run in the cloud`.

You can have Codex run off main—which is useful for starting new ideas—or instead you can have Codex work from your local changes—useful for finishing off a task.

![codex-cloud-task](/images/codex/ide/start_cloud_task.png)

When you start a cloud task from a local conversation, Codex remembers the conversation context so it can pick up where you left off.

## Follow up on cloud tasks

The Codex extension makes previewing cloud changes easy. You can ask for followups to be done in the cloud, but often you'll want to apply the changes down locally to test and finish up. When continuing the conversation locally, Codex also retains context to save you time.

![](/images/codex/ide/load_cloud_task.png)

You can also view the cloud tasks in the [Codex interface](https://chatgpt.com/codex).

## Next steps

To learn more about how to use Codex in the cloud, refer to our [dedicated guide](/codex/cloud).

You can experiment to find your preferred workflow: you can stay in the IDE with the Codex extension for tasks you're currently focusing on, and delegate everything else to the cloud agent.
You can then follow progress in the Codex interface or in the IDE depending on your preferences.
