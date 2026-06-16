---
source_url: http://geminicli.com/docs/get-started
source_type: llms-txt
content_hash: sha256:ff6cdec93ec3ac4e7e2e7f8ece121d8aec52a528ca09c1227641baa3bd748ace
sitemap_url: https://geminicli.com/llms.txt
fetch_method: markdown
etag: '"561b529326241903e6337dc9e9bc3f96535f6cd252d054dc7d1f1b9d268fd272"'
last_modified: '2026-03-16T19:53:24Z'
---

# Get started with Gemini CLI

Welcome to Gemini CLI! This guide will help you install, configure, and start
using the Gemini CLI to enhance your workflow right from your terminal.

## Quickstart: Install, authenticate, configure, and use Gemini CLI

Gemini CLI brings the power of advanced language models directly to your command
line interface. As an AI-powered assistant, Gemini CLI can help you with a
variety of tasks, from understanding and generating code to reviewing and
editing documents.

## Install

The standard method to install and run Gemini CLI uses `npm`:

```bash
npm install -g @google/gemini-cli
```

Once Gemini CLI is installed, run Gemini CLI from your command line:

```bash
gemini
```

For more installation options, see [Gemini CLI Installation](/docs/get-started/installation).

## Authenticate

To begin using Gemini CLI, you must authenticate with a Google service. In most
cases, you can log in with your existing Google account:

1. Run Gemini CLI after installation:

   ```bash
   gemini
   ```

2. When asked "How would you like to authenticate for this project?" select **1.
   Sign in with Google**.

3. Select your Google account.

4. Click on **Sign in**.

Certain account types may require you to configure a Google Cloud project. For
more information, including other authentication methods, see
[Gemini CLI Authentication Setup](/docs/get-started/authentication).

## Configure

Gemini CLI offers several ways to configure its behavior, including environment
variables, command-line arguments, and settings files.

To explore your configuration options, see
[Gemini CLI Configuration](/docs/reference/configuration).

## Use

Once installed and authenticated, you can start using Gemini CLI by issuing
commands and prompts in your terminal. Ask it to generate code, explain files,
and more.

To explore the power of Gemini CLI, see [Gemini CLI examples](/docs/get-started/examples).

## Check usage and quota

You can check your current token usage and quota information using the
`/stats model` command. This command provides a snapshot of your current
session's token usage, as well as your overall quota and usage for the supported
models.

For more information on the `/stats` command and its subcommands, see the
[Command Reference](/docs/reference/commands#stats).

## Next steps

- Follow the [File management](/docs/cli/tutorials/file-management) guide to
  start working with your codebase.
- See [Shell commands](/docs/cli/tutorials/shell-commands) to learn about
  terminal integration.
