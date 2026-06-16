---
source_url: http://geminicli.com/docs/cli/notifications
source_type: llms-txt
content_hash: sha256:fe65e46e76e2d31d31780f927c1138b95e91f03121457fc148a2a69f39afd5b3
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"9b3aea965430cf36d201a15584e18c2f524f702ca66f11c56330636c8a201ae4"'
last_modified: '2026-03-22T19:06:33Z'
---

# Notifications (experimental)

Gemini CLI can send system notifications to alert you when a session completes
or when it needs your attention, such as when it's waiting for you to approve a
tool call.

<!-- prettier-ignore -->
> [!NOTE]
> This is an experimental feature currently under active development and
> may need to be enabled under `/settings`.

Notifications are particularly useful when running long-running tasks or using
[Plan Mode](/docs/cli/plan-mode), letting you switch to other windows while Gemini
CLI works in the background.

## Requirements

Currently, system notifications are only supported on macOS.

### Terminal support

The CLI uses the OSC 9 terminal escape sequence to trigger system notifications.
This is supported by several modern terminal emulators. If your terminal does
not support OSC 9 notifications, Gemini CLI falls back to a system alert sound
to get your attention.

## Enable notifications

Notifications are disabled by default. You can enable them using the `/settings`
command or by updating your `settings.json` file.

1.  Open the settings dialog by typing `/settings` in an interactive session.
2.  Navigate to the **General** category.
3.  Toggle the **Enable Notifications** setting to **On**.

Alternatively, add the following to your `settings.json`:

```json
{
  "general": {
    "enableNotifications": true
  }
}
```

## Types of notifications

Gemini CLI sends notifications for the following events:

- **Action required:** Triggered when the model is waiting for user input or
  tool approval. This helps you know when the CLI has paused and needs you to
  intervene.
- **Session complete:** Triggered when a session finishes successfully. This is
  useful for tracking the completion of automated tasks.

## Next steps

- Start planning with [Plan Mode](/docs/cli/plan-mode).
- Configure your experience with other [settings](/docs/cli/settings).
