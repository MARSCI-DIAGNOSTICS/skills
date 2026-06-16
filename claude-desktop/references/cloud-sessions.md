# Cloud Sessions

## Overview

Claude Desktop can launch Claude Code sessions on **Anthropic's secure cloud infrastructure** instead of running locally.

## Starting a Cloud Session

1. Open Claude Desktop
2. Click to create a new session
3. Select **"Remote environment"** instead of "Local"
4. Session runs on Anthropic infrastructure

## Commands

### /teleport

Teleport an existing session to cloud execution.

```text
/teleport
```

**Use cases:**

- Move a resource-intensive task to cloud
- Access more compute power
- Continue work on a different machine

### /remote-env

Configure remote environment settings.

```text
/remote-env
```

**Note:** Available for claude.ai subscribers.

## Desktop vs CLI

| Aspect | Claude Desktop | Claude Code CLI |
| --- | --- | --- |
| **Interface** | Graphical | Command-line |
| **Best For** | Beginners, non-coders, deliberate workflows | Professional devs, automation |
| **Control Level** | Higher (each action requires approval) | Agentic (takes initiative) |
| **Features** | Stability-focused | Newer features first |
| **IDE Integration** | Via desktop app | Native (VS Code, JetBrains) |
| **Worktrees** | Built-in GUI | Manual via CLI |

### When to Use Desktop

- Learning to code
- Productivity tasks (documentation, spreadsheets, emails)
- Maximum control over each step
- Writing documents, slide decks, PDFs
- Deliberate, back-and-forth workflows

### When to Use CLI

- Professional development
- Integration with VS Code or JetBrains
- Direct terminal access needed
- Running tests, builds, deployments
- Git operations and commits
- Complex automation tasks

## Cloud vs Local Sessions

| Aspect | Local Session | Cloud Session |
| --- | --- | --- |
| Execution | Your machine | Anthropic infrastructure |
| Resources | Your CPU/RAM | Cloud resources |
| File Access | Full local access | Limited to workspace |
| Network | Your network | Anthropic network |
| Cost | Included | May have usage limits |

## Benefits of Cloud Sessions

- **No local resource consumption** - Heavy tasks don't slow your machine
- **Secure infrastructure** - Anthropic-managed security
- **Consistent environment** - Same environment regardless of your machine
- **Cross-device** - Continue on another device

## Limitations

- **File access** - Limited to files uploaded/synced to session
- **Network** - May not have access to local network resources
- **Latency** - Slightly higher than local execution
- **Windows ARM64** - Local sessions not available, cloud-only

## Related Topics

- [Setup Guide](setup-guide.md) - Installation
- [Troubleshooting](troubleshooting.md) - Common issues
