---
name: plugin-development
description: Central authority for Claude Code plugins. Covers plugin creation, plugin structure (plugin.json, commands/, agents/, skills/, hooks/), plugin manifest configuration, plugin installation and management (/plugin command), plugin marketplaces (marketplace.json, adding marketplaces), team plugin workflows, plugin development and testing, plugin debugging, plugin sharing and distribution, MCP servers in plugins, and plugin settings. Assists with creating plugins, installing from marketplaces, configuring team plugins, and troubleshooting plugin issues. Delegates 100% to docs-management skill for official documentation.
user-invocable: false
allowed-tools: Read, Glob, Grep, Skill
---

# Plugins Meta Skill

## 🚨 MANDATORY: Invoke docs-management First

> **STOP - Before providing ANY response about Claude Code plugins:**
>
> 1. **INVOKE** `docs-management` skill
> 2. **QUERY** for the user's specific topic
> 3. **BASE** all responses EXCLUSIVELY on official documentation loaded
>
> **Skipping this step results in outdated or incorrect information.**

### Verification Checkpoint

Before responding, verify:

- [ ] Did I invoke docs-management skill?
- [ ] Did official documentation load?
- [ ] Is my response based EXCLUSIVELY on official docs?

If ANY checkbox is unchecked, STOP and invoke docs-management first.

---

## Overview

Central authority for Claude Code plugins. This skill uses **100% delegation to docs-management** - it contains NO duplicated official documentation.

**Architecture:** Pure delegation with keyword registry. All official documentation is accessed via docs-management skill queries.

## When to Use This Skill

**Keywords:** plugins, plugin creation, plugin structure, plugin.json, plugin manifest, plugin commands, plugin agents, plugin skills, plugin hooks, plugin marketplaces, marketplace.json, /plugin command, plugin install, plugin uninstall, plugin enable, plugin disable, plugin browse, team plugins, plugin development, plugin testing, plugin debugging, plugin sharing, plugin distribution, MCP servers plugins, plugin settings, enabledPlugins, extraKnownMarketplaces, plugin hook configuration, disable plugin hook, CLAUDE_HOOK_ENABLED, hook environment variables, configurable hooks, hook enforcement mode

**Use this skill when:**

- Creating new plugins
- Understanding plugin structure and components
- Writing plugin manifest (plugin.json)
- Adding commands, agents, skills, hooks to plugins
- Installing plugins from marketplaces
- Managing plugin marketplaces
- Setting up team plugin workflows
- Testing plugins locally
- Debugging plugin issues
- Sharing and distributing plugins
- Configuring MCP servers in plugins
- Managing plugin settings
- **Registering plugins in marketplace.json** (CRITICAL for distribution)
- **Configuring plugin hooks for consumers to enable/disable**
- **Making plugin hooks configurable via environment variables**

## Keyword Registry for docs-management Queries

Use these keywords when querying docs-management skill for official documentation:

### Plugin Fundamentals

| Topic | Keywords |
| --- | --- |
| Overview | "plugins", "plugin system", "extend Claude Code" |
| Quickstart | "plugin quickstart", "first plugin", "create plugin" |
| Structure | "plugin structure", "plugin directory structure" |
| Manifest | "plugin.json", "plugin manifest", "plugin metadata" |

### Plugin Components

| Topic | Keywords |
| --- | --- |
| Commands | "plugin commands", "commands directory plugins" |
| Agents | "plugin agents", "agents directory plugins" |
| Skills | "plugin skills", "skills directory plugins" |
| Hooks | "plugin hooks", "hooks.json plugins" |
| MCP Servers | "MCP servers plugins", ".mcp.json plugins" |

### Plugin Installation

| Topic | Keywords |
| --- | --- |
| Install Commands | "/plugin command", "plugin install", "plugin management" |
| Enable/Disable | "plugin enable", "plugin disable", "plugin uninstall" |
| Interactive Menu | "plugin browse", "/plugin interactive" |
| Verification | "verify plugin installation", "plugin /help" |

### Plugin Marketplaces

| Topic | Keywords |
| --- | --- |
| Overview | "plugin marketplaces", "marketplace catalogs" |
| Adding Marketplaces | "marketplace add", "add marketplaces" |
| Marketplace Manifest | "marketplace.json", "marketplace manifest" |
| Marketplace Sources | "plugin sources", "marketplace sources" |
| Schema Fields | "metadata.pluginRoot", "strict field marketplace", "plugin entry schema" |
| Reserved Names | "reserved marketplace name", "marketplace name validation" |

### Team Configuration

| Topic | Keywords |
| --- | --- |
| Team Plugins | "team plugin workflows", "repository-level plugins" |
| Auto Installation | "automatic plugin installation", "team plugins setup" |
| Configuration | "team marketplaces configuration", ".claude/settings.json plugins" |

### Plugin Development

| Topic | Keywords |
| --- | --- |
| Development Workflow | "plugin development", "develop plugins" |
| Local Testing | "test plugins locally", "local marketplace" |
| Iteration | "plugin iteration", "reinstall plugin" |
| Organization | "organize complex plugins", "plugin organization" |
| Environment Variables | "CLAUDE_PLUGIN_ROOT", "plugin environment variables" |

### Debugging and Troubleshooting

| Topic | Keywords |
| --- | --- |
| Debugging | "debug plugin issues", "plugin debugging" |
| Debug Mode | "claude --debug", "plugin loading debug" |
| Validation | "plugin validation", "claude plugin validate" |
| Common Issues | "plugin not working", "plugin troubleshooting" |

### Distribution

| Topic | Keywords |
| --- | --- |
| Sharing | "share plugins", "plugin distribution" |
| Documentation | "plugin documentation", "plugin README" |
| Versioning | "plugin versioning", "semantic versioning plugins" |
| Marketplace Registration | "marketplace.json", "register plugin", "plugin entry", "marketplace plugins array" |

### Settings and Configuration

| Topic | Keywords |
| --- | --- |
| Plugin Settings | "plugin settings", "enabledPlugins" |
| Marketplace Settings | "extraKnownMarketplaces", "marketplace configuration" |

### Plugin Hook Configuration

| Topic | Keywords |
| --- | --- |
| Hook Basics | "plugin hooks", "hooks.json plugins" |
| Auto-Discovery | "hooks auto-discovery", "default hooks location", "hooks.json default" |
| Manifest Format | "hooks field format", "hooks path", "hooks.json path" |
| Consumer Control | "disable plugin hook", "hook environment variables" |
| Enforcement Modes | "hook enforcement mode", "CLAUDE_HOOK_ENFORCEMENT" |
| Disable Hooks | "CLAUDE_HOOK_ENABLED", "disable specific hook" |

**Note:** Plugin hook configuration uses environment variables (not YAML configs like local hooks). See [Plugin Hook Utilities Reference](references/plugin-hook-utilities.md) for implementation patterns and [Consumer Configuration Reference](references/plugin-hook-consumer-config.md) for end-user guidance.

### Component Discovery & Validation

| Topic | Keywords |
| --- | --- |
| Auto-Discovery | "plugin auto-discovery", "default locations", "component discovery" |
| Default Paths | "plugin default paths", "default directory", "path behavior" |
| Optional Fields | "plugin optional fields", "required vs optional", "manifest optional" |
| Path Formats | "component path fields", "path format", "hooks path format" |
| Field Validation | "plugin field validation", "manifest validation", "field format" |

### Reference

| Topic | Keywords |
| --- | --- |
| Technical Reference | "plugins reference", "plugin specifications" |
| Component Reference | "plugin components reference", "plugin schemas" |
| Manifest Path Fields | "component path fields", "custom plugin paths", "path behavior rules" |

## Quick Decision Tree

**What do you want to do?**

1. **Create a new plugin** -> Query docs-management: "plugin quickstart", "create plugin"
2. **Understand plugin structure** -> Query docs-management: "plugin structure", "plugin directory structure"
3. **Write plugin manifest** -> Query docs-management: "plugin.json", "plugin manifest"
4. **Add commands to plugin** -> Query docs-management: "plugin commands", "commands directory plugins"
5. **Add agents to plugin** -> Query docs-management: "plugin agents", "agents directory plugins"
6. **Add skills to plugin** -> Query docs-management: "plugin skills", "skills directory plugins"
7. **Add hooks to plugin** -> Query docs-management: "plugin hooks", "hooks.json plugins"
8. **Install a plugin** -> Query docs-management: "/plugin command", "plugin install"
9. **Add a marketplace** -> Query docs-management: "marketplace add", "plugin marketplaces"
10. **Set up team plugins** -> Query docs-management: "team plugin workflows"
11. **Test plugin locally** -> Query docs-management: "test plugins locally"
12. **Debug plugin issues** -> Query docs-management: "debug plugin issues", "plugin troubleshooting"
13. **Validate plugin structure** -> Query docs-management: "claude plugin validate", "plugin validation"
14. **Debug plugin loading** -> Query docs-management: "claude --debug", "plugin loading debug"
15. **Register plugin in marketplace** -> Query docs-management: "marketplace.json", "register plugin"
16. **Make hooks configurable** -> See [Plugin Hook Utilities Reference](references/plugin-hook-utilities.md)
17. **Disable a plugin's hook** -> See [Consumer Configuration Reference](references/plugin-hook-consumer-config.md)
18. **Complete plugin reset** -> Run `/user-config:reset-plugins` (clears cache + registry + settings)

## Topic Coverage

### Plugin Structure

- .claude-plugin/ directory
- plugin.json manifest file
- agents/ directory for subagents
- skills/ directory for skills
- hooks/ directory with hooks.json
- .mcp.json for MCP servers

### Component Auto-Discovery & Default Locations

Plugin components may be auto-discovered from default locations. Query docs-management for current behavior:

**Query Keywords:**

- "plugin auto-discovery", "default locations", "component discovery"
- "plugin default paths", "path behavior rules"
- "hooks default location", "commands default location"
- "plugin optional fields", "required vs optional"

**Key Principle:** Before flagging missing manifest fields, query docs-management to verify whether the component uses auto-discovery from a default location. Many manifest fields are optional when components exist at their default paths.

### Plugin Manifest (plugin.json)

- name field (required)
- description field
- version field (semantic versioning)
- author object
- Additional metadata fields

### Plugin Component Types

- Agents (markdown files in agents/)
- Skills (SKILL.md files in skills/)
- Hooks (hooks.json configuration)
- MCP servers (.mcp.json configuration)

### Plugin Installation Commands

- /plugin (interactive menu)
- /plugin install plugin-name@marketplace
- /plugin uninstall plugin-name@marketplace
- /plugin enable plugin-name@marketplace
- /plugin disable plugin-name@marketplace
- /plugin marketplace add

### Marketplace Configuration

- marketplace.json structure
- name and owner fields
- plugins array with source references
- Local vs remote marketplace sources
- Git repository marketplaces

### Team Plugin Workflows

- Repository-level configuration (.claude/settings.json)
- Automatic installation on trust
- Team-wide plugin consistency
- Rollout best practices

### Development Workflow

- Local marketplace setup
- Development directory structure
- Plugin iteration cycle (uninstall/reinstall)
- Testing components individually

### Debugging Techniques

- Structure verification
- Component isolation testing
- Validation tools
- Common issue resolution

### Distribution Strategies

- README documentation
- Semantic versioning
- Marketplace submission
- Team testing before release
- **Marketplace registration** (see below)

### Marketplace Registration (CRITICAL)

**⚠️ ALWAYS register new plugins in marketplace.json** - plugins are NOT discoverable until registered.

**When creating a new plugin, you MUST:**

1. Create the plugin structure (`.claude-plugin/plugin.json`, components)
2. Register the plugin in `marketplace.json` with proper entry format
3. Verify registration by checking `/plugin` command lists the new plugin

**Query docs-management for current marketplace.json schema:**

- Keywords: "marketplace.json", "marketplace plugins array", "plugin entry schema"
- This ensures you use the current format (schema may evolve)

**Common oversight:** Creating a plugin but forgetting to add it to marketplace.json - the plugin will exist but be invisible to users.

### Component Registration in plugin.json (CRITICAL)

**⚠️ ALWAYS check plugin.json when adding new agents, commands, or skills** - the manifest may use explicit arrays instead of directory auto-discovery.

**Two Registration Modes:**

| Mode | plugin.json Syntax | Behavior |
| --- | --- | --- |
| **Directory (auto-discovery)** | `"agents": "./agents"` | All `.md` files in directory are loaded automatically |
| **Explicit array** | `"agents": ["./agents/foo.md", "./agents/bar.md"]` | ONLY listed files are loaded - new files IGNORED |

**When to register manually:**

1. Check `plugin.json` for the component type you're adding
2. If it's an **explicit array** → Add your new file to the array
3. If it's a **directory path** → No action needed (auto-discovered)

**Common oversight:** Creating a new agent file but forgetting to add it to the `agents` array in `plugin.json` - the file will exist but the agent won't load (silent failure, no error message).

**Example (explicit array):**

```json
{
  "agents": [
    "./agents/existing-agent.md",
    "./agents/new-agent.md"  // <-- ADD THIS LINE
  ]
}
```

**Why this matters:** Claude Code v2.1.x doesn't provide error messages when agents aren't registered - they simply don't appear in the available agents list.

### Plugin Data Locations (Two-Location Architecture)

> **Documentation Verification:** Query `docs-management: "plugin cache plugin storage locations"` for current
> Claude Code plugin data locations. The paths below were accurate at time of writing but may change between releases.

**IMPORTANT:** Plugin data is stored in TWO locations. Both must be cleared for a complete reset:

| Location | Contains | Cleared By |
| --- | --- | --- |
| `~/.claude/plugins/` | Plugin cache, registry, marketplace cache | `/clear-plugin-cache` (partial), `/user-config:reset-plugins` (complete) |
| `~/.claude/settings.json` → `enabledPlugins` | Plugin enable/disable state | `/user-config:reset-plugins` only |

**Common Confusion:** `/clear-plugin-cache` only clears the cache directory, preserving the registry. If you see "Plugin not found in marketplace" errors after cache clearing, the `enabledPlugins` in settings.json still references the old plugins.

**Solution:** Use `/user-config:reset-plugins` for complete plugin reset.

### Settings Integration

- enabledPlugins configuration
- extraKnownMarketplaces configuration
- Plugin-related settings in settings.json

### Plugin Hook Configuration (Repository-Specific)

Plugin hooks are automatically merged when a plugin is enabled. Unlike local hooks (`.claude/hooks/`), plugin hooks use **environment variables** for consumer control:

**Environment Variable Convention:**

| Variable | Values | Purpose |
| --- | --- | --- |
| `CLAUDE_HOOK_{NAME}_ENABLED` | `1`/`true` (enabled), `0`/`false` (disabled) | Enable/disable hook |
| `CLAUDE_HOOK_ENFORCEMENT_{NAME}` | `block`, `warn`, `log` | Control enforcement behavior |
| `CLAUDE_HOOK_LOG_LEVEL` | `debug`, `info`, `warn`, `error` | Logging verbosity |

**Consumer Configuration via settings.json:**

```json
{
  "env": {
    "CLAUDE_HOOK_MARKDOWN_LINT_ENABLED": "1",
    "CLAUDE_HOOK_ENFORCEMENT_SECRET_SCAN": "warn"
  }
}
```

**For Plugin Authors:** See [Plugin Hook Utilities Reference](references/plugin-hook-utilities.md)
**For Plugin Consumers:** See [Consumer Configuration Reference](references/plugin-hook-consumer-config.md)

## Delegation Patterns

### Standard Query Pattern

```text
User asks: "How do I create a plugin?"

1. Invoke docs-management skill
2. Use keywords: "plugin quickstart", "create plugin"
3. Load official documentation
4. Provide guidance based EXCLUSIVELY on official docs
```

### Multi-Topic Query Pattern

```text
User asks: "I want to create a plugin with commands, hooks, and MCP servers"

1. Invoke docs-management skill with multiple queries:
   - "plugin structure", "plugin.json"
   - "plugin commands", "commands directory plugins"
   - "plugin hooks", "hooks.json plugins"
   - "MCP servers plugins", ".mcp.json plugins"
2. Synthesize guidance from official documentation
```

### Troubleshooting Pattern

```text
User reports: "My plugin commands aren't showing up"

1. Invoke docs-management skill
2. Use keywords: "debug plugin issues", "verify plugin installation"
3. Check official docs for plugin structure requirements
4. Guide user through debugging based on official docs
```

## Troubleshooting Quick Reference

| Issue | Keywords for docs-management |
| --- | --- |
| Plugin not installing | "/plugin command", "plugin install" |
| Commands not appearing | "plugin commands", "verify plugin installation" |
| Agents not available | "plugin agents", "agents directory plugins" |
| Hooks not triggering | "plugin hooks", "hooks.json plugins" |
| Marketplace not found | "marketplace add", "plugin marketplaces" |
| Team plugins not syncing | "team plugin workflows", "automatic plugin installation" |
| Plugin structure invalid | "plugin structure", "debug plugin issues" |
| MCP server not starting | "MCP servers plugins", "CLAUDE_PLUGIN_ROOT" |
| Custom paths not loading | "component path fields", "path behavior rules" |
| Plugin validation errors | "claude plugin validate", "plugin validation" |
| Hook not running | Check CLAUDE_HOOK_{NAME}_ENABLED env var in settings.json |
| Hook enforcement wrong | Check CLAUDE_HOOK_ENFORCEMENT_{NAME} env var in settings.json |
| "hooks: must end with .json" | hooks field must be file path (e.g., "./hooks.json"), not directory |
| "Name is reserved" error | See [Reserved Marketplace Names Reference](references/reserved-marketplace-names.md) |
| Plugin not showing in /plugin | Check if registered in marketplace.json - see [Marketplace Registration](#marketplace-registration-critical) |
| Plugin errors after clearing cache | Plugin data in TWO locations: `~/.claude/plugins/` AND `enabledPlugins` in `~/.claude/settings.json` - use `/user-config:reset-plugins` for complete reset |

## Repository-Specific Notes

This repository does not currently use plugins. Plugin documentation is relevant for:

- Understanding how plugins extend Claude Code functionality
- Potential future plugin development for this repository
- Understanding plugin-based distribution of commands, agents, skills, and hooks

When working with plugin topics, always use the docs-management skill to access official documentation.

### Reserved Marketplace Names

See [Reserved Marketplace Names Reference](references/reserved-marketplace-names.md) for:

- Known reserved names that cause "Name is reserved" errors
- How to fix marketplace.json when encountering this error
- Migration guidance for existing installations

## Auditing Plugins

This skill provides the validation criteria used by the `plugin-component-auditor` agent for formal audits.

### Audit Resources

| Resource | Location | Purpose |
| --- | --- | --- |
| Audit Framework | `references/audit-framework.md` | Query guides and scoring criteria |

### Scoring Categories

| Category | Points | Key Criteria |
| --- | --- | --- |
| Manifest Structure | 25 | Valid plugin.json, required fields |
| Component Organization | 25 | Proper directories for all components |
| Namespace Compliance | 20 | Consistent naming, no conflicts |
| Documentation | 15 | README, descriptions, examples |
| Distribution Readiness | 15 | Version, marketplace requirements |

**Thresholds:** 85+ = PASS, 70-84 = PASS WITH WARNINGS, <70 = FAIL

### Related Agent

The `plugin-component-auditor` agent (Haiku model) performs formal audits using this skill:

- Auto-loads this skill via `skills: plugin-development`
- Uses audit framework and docs-management for rules
- Generates structured audit reports
- Invoked by `/audit-plugins` command

### External Technology Validation

When auditing plugins that use external technologies (scripts, packages, runtimes), the auditor MUST validate claims using MCP servers before flagging findings.

**Technologies Requiring MCP Validation:**

- .NET/C# scripts: Validate with microsoft-learn + perplexity
- Node.js/npm packages: Validate with context7 + perplexity
- Python scripts/packages: Validate with context7 + perplexity
- Shell scripts: Validate with perplexity
- Any version-specific claims: ALWAYS validate with perplexity

**Validation Rule:**

Never flag a technology usage as incorrect without first:

1. Querying appropriate MCP server(s) for current documentation
2. Verifying with perplexity for recent changes (especially .NET 10+)
3. Documenting MCP sources in the finding

**Stale Data Warning:**

- microsoft-learn can return cached/outdated documentation
- ALWAYS pair microsoft-learn with perplexity for version verification
- Trust perplexity for version numbers and recently-released features

## References

**Official Documentation (via docs-management skill):**

- Primary: "plugins", "plugins-reference", "plugin-marketplaces" documentation
- Related: "skills", "sub-agents", "hooks", "mcp", "settings"

**Repository-Specific:**

- Plugin settings: `.claude/settings.json` (enabledPlugins, extraKnownMarketplaces)
- [Plugin Hook Utilities Reference](references/plugin-hook-utilities.md) - For plugin authors implementing configurable hooks
- [Consumer Configuration Reference](references/plugin-hook-consumer-config.md) - For plugin consumers controlling hook behavior

## Version History

- **v1.3.3** (2026-01-10): Added component registration documentation
  - Added "Component Registration in plugin.json (CRITICAL)" section
  - Documents explicit array vs directory auto-discovery modes
  - Added detection and fix guidance for missing agent registration
  - Cross-referenced from subagent-development skill
- **v1.3.2** (2025-12-30): Added plugin reset documentation
  - Added "Plugin Data Locations (Two-Location Architecture)" section
  - Added Quick Decision Tree entry for complete plugin reset (entry 18)
  - Added troubleshooting entry for plugin errors after clearing cache
  - Documents two-location architecture and `/user-config:reset-plugins` command
- **v1.3.1** (2025-12-26): Added marketplace registration reminder
  - Added "Marketplace Registration (CRITICAL)" section to Topic Coverage
  - Added marketplace registration to Quick Decision Tree (entry 15)
  - Added "Marketplace Registration" to Distribution keyword registry
  - Added troubleshooting entry for "Plugin not showing in /plugin"
  - Updated "When to Use This Skill" to include marketplace registration
  - Emphasizes querying docs-management for current marketplace.json schema
- **v1.3.0** (2025-12-25): Expanded docs-management delegation for component discovery
  - Added "Component Auto-Discovery & Default Locations" section with query keywords
  - Expanded keyword registry with auto-discovery, default paths, optional fields, path formats
  - Added troubleshooting entry for "hooks: must end with .json" error
  - Enhanced audit-framework.md with expanded Documentation Query Guide
  - Added "Validation Protocol" section enforcing docs-first validation
  - All component validation now requires docs-management verification before flagging issues
- **v1.2.1** (2025-12-16): Reserved marketplace names documentation
  - Added "Reserved Marketplace Names (Undocumented)" section documenting runtime validation
  - Added troubleshooting entry for "Name is reserved" error
  - Added keyword entry for reserved names topic
  - Documents that `claude-code-plugins` name is reserved for `anthropics` organization
- **v1.2.0** (2025-12-01): Environment variable standardization
  - Updated to `CLAUDE_HOOK_{NAME}_ENABLED` pattern (from deprecated `CLAUDE_HOOK_DISABLED_*`)
  - Updated all documentation, examples, and references to new pattern
  - Updated plugin-hook-utilities.md with new `is_hook_enabled()` function supporting defaults
  - Updated plugin-hook-consumer-config.md with new configuration examples
  - Updated troubleshooting entries for new pattern
- **v1.1.0** (2025-11-30): Plugin hook configuration documentation
  - Added Plugin Hook Configuration section to keyword registry
  - Added topic coverage for hook configuration patterns (env vars, enforcement modes)
  - Added decision tree paths: make hooks configurable, disable plugin hooks
  - Added troubleshooting entries for hook configuration issues
  - Created references directory with plugin-hook-utilities.md and plugin-hook-consumer-config.md
- **v1.0.1** (2025-11-27): Minor enhancements
  - Added keywords: CLAUDE_PLUGIN_ROOT, claude --debug, claude plugin validate, marketplace schema fields, path behavior rules
  - Expanded decision tree: +2 paths (validate plugin structure, debug plugin loading)
  - Expanded troubleshooting: +3 entries (MCP server, custom paths, validation errors)
- **v1.0.0** (2025-11-26): Initial release
  - Pure delegation architecture
  - Comprehensive keyword registry
  - Quick decision tree
  - Topic coverage for all plugin features
  - Troubleshooting quick reference

---

## Last Updated

**Date:** 2026-01-10
**Model:** claude-opus-4-5-20251101
