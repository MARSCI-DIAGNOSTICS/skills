---
source_url: https://cursor.com/help/customization/mcp
source_type: llms-txt
content_hash: sha256:e7176fb4fd9835b0b6b94928ac4cfa896c0c0b2494a92855efaeeee7be6e9862
sitemap_url: https://cursor.com/llms.txt
fetch_method: markdown
---

# MCP integrations

MCP (Model Context Protocol) connects Cursor to external tools and data sources. Integrate with databases, APIs, and services like GitHub, Linear, or Notion so Agent can use them during conversations.

## What is an MCP server?

An MCP server exposes tools and data sources to Cursor through the Model Context Protocol. Agent can call those tools directly during a chat.

## Does Cursor support MCP Apps?

Yes. Cursor supports the [MCP Apps extension](https://modelcontextprotocol.io/extensions/apps/overview), so MCP tools can return interactive UI in chat.

If app UI is unavailable, the same tool still works through normal MCP responses.

## How do I install an MCP server (one-click)?

1. Open Cursor Settings:
   - **Mac**: Press Cmd + Shift + J
   - **Windows/Linux**: Press Ctrl + Shift + J
2. Click **Tools & MCP** in the sidebar
3. Browse available servers or search for the one you want
4. Click **Add to Cursor** next to the server
5. Follow the authentication prompts if required

The server is now connected. Agent uses its tools when relevant to your requests.

## How do I install an MCP server manually?

Create a file called `mcp.json` in one of these locations:

- **Project-specific** (shared with your team): `.cursor/mcp.json` in your project folder. Commit this to git so teammates get the same tools.
- **Global** (personal, all projects): `~/.cursor/mcp.json` in your home directory

Both files are merged. If the same server name appears in both, the project-level config takes priority.

For local servers, add your server config with a `command`:

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "mcp-server"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

Some MCP servers (like hosted databases or custom APIs) provide a URL instead of a local command. Add them using the `url` field:

```json
{
  "mcpServers": {
    "my-service": {
      "url": "https://mcp.example.com/sse"
    }
  }
}
```

If the server requires authentication headers, add them under `headers`:

```json
{
  "mcpServers": {
    "my-service": {
      "url": "https://mcp.example.com/sse",
      "headers": {
        "Authorization": "Bearer your-token-here"
      }
    }
  }
}
```

Save the file and restart Cursor.

## How do I use MCP tools in chat?

Agent picks up MCP tools automatically and uses them when relevant. Toggle tools on or off by clicking the tool name in the tools list at the top of the chat panel.

By default, Agent asks for your approval before using an MCP tool. Enable auto-run in settings if you prefer Agent to use tools without asking.

## How do I troubleshoot MCP servers?

- **View logs**: Open the Output panel (Cmd + Shift + U on Mac, Ctrl + Shift + U on Windows/Linux) and select **MCP Logs**
- **Toggle servers**: Open Settings (Cmd + Shift + J) > **Tools & MCP**. Click the toggle next to any server.
- **Restart**: Remove the server from settings, then re-add it
- **Environment variables**: If your server relies on environment variables set in your shell profile, make sure those variables are available to Cursor. Restart Cursor after updating your shell profile.

## Do MCP servers work with Cloud Agents?

Yes. Cloud Agents support MCP servers configured in the [Cloud Agents dashboard](https://cursor.com/agents). On a Team plan, you can also configure shared MCP servers for your team under [Settings > Integrations](https://cursor.com/dashboard?tab=integrations). See [Cloud Agent MCP tools](https://cursor.com/docs/cloud-agent/capabilities.md#mcp-tools) for more details.

## Where can I find MCP servers to install?

Browse the [Cursor Marketplace](/marketplace) for official plugins and one-click installation. For community plugins and MCP servers, browse [cursor.directory](https://cursor.directory).

## Related

- [MCP reference](https://cursor.com/docs/mcp.md)
- [Cursor Marketplace](/marketplace)
- [cursor.directory](https://cursor.directory)
- [Cloud Agents](https://cursor.com/help/ai-features/cloud-agents.md)


---

## Sitemap

[Overview of all docs pages](/llms.txt)
