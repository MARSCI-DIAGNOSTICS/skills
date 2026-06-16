# -*- coding: utf-8 -*-
"""Shared pytest fixtures for schema script tests."""

import pytest


@pytest.fixture
def sample_settings_md() -> str:
    """Sample settings.md content for testing extraction."""
    return """
## Environment variables

| Variable | Description |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API key sent as X-Api-Key header, typically for the Claude SDK |
| `ANTHROPIC_MODEL` | Name of the model setting to use. See [Model Configuration](/docs/model-configuration) |
| `DISABLE_TELEMETRY` | Set to 1 to opt out of Statsig telemetry |
| `BASH_DEFAULT_TIMEOUT_MS` | Default timeout for long-running bash commands (milliseconds) |
| `CLAUDE_CODE_USE_BEDROCK` | Use Amazon Bedrock as the LLM provider |
| `ANTHROPIC_SMALL_FAST_MODEL` | [DEPRECATED] Name of Haiku-class model for background tasks |
| `HTTP_PROXY` | Specify HTTP proxy server for network connections |
| `MCP_TIMEOUT` | Timeout in milliseconds for MCP server startup |
| `VERTEX_REGION_CLAUDE_4_0_OPUS` | Override region for Claude 4.0 Opus when using Vertex AI |
"""


@pytest.fixture
def sample_changelog_md() -> str:
    """Sample CHANGELOG.md content for testing extraction."""
    return """
# Changelog

## 2.1.5

- Added `CLAUDE_CODE_TMPDIR` environment variable for temp directory override

## 2.1.4

- Added `CLAUDE_CODE_DISABLE_BACKGROUND_TASKS` to disable background task functionality

## 2.1.0

- New environment variable `CLAUDE_SESSION_ID` for session tracking
"""


@pytest.fixture
def known_env_vars() -> dict:
    """Known env vars with their expected categories and types."""
    return {
        # Authentication
        "ANTHROPIC_API_KEY": {"category": "authentication", "type": None},
        "ANTHROPIC_AUTH_TOKEN": {"category": "authentication", "type": None},
        "AWS_BEARER_TOKEN_BEDROCK": {"category": "authentication", "type": None},
        # Model config
        "ANTHROPIC_MODEL": {"category": "model-config", "type": None},
        "ANTHROPIC_DEFAULT_HAIKU_MODEL": {"category": "model-config", "type": None},
        # Provider
        "CLAUDE_CODE_USE_BEDROCK": {"category": "provider", "type": "boolean"},
        "CLAUDE_CODE_SKIP_VERTEX_AUTH": {"category": "provider", "type": "boolean"},
        # Bash behavior
        "BASH_DEFAULT_TIMEOUT_MS": {"category": "bash-behavior", "type": "integer"},
        "CLAUDE_CODE_SHELL": {"category": "bash-behavior", "type": None},
        # Disable flags
        "DISABLE_TELEMETRY": {"category": "disable-flags", "type": "boolean"},
        "CLAUDE_CODE_DISABLE_TERMINAL_TITLE": {"category": "disable-flags", "type": "boolean"},
        # Proxy
        "HTTP_PROXY": {"category": "proxy", "type": None},
        "HTTPS_PROXY": {"category": "proxy", "type": None},
        # MCP
        "MCP_TIMEOUT": {"category": "mcp", "type": "integer"},
        "MAX_MCP_OUTPUT_TOKENS": {"category": "mcp", "type": "integer"},
        # Vertex/Bedrock
        "VERTEX_REGION_CLAUDE_4_0_OPUS": {"category": "vertex-bedrock", "type": None},
        # Tools
        "SLASH_COMMAND_TOOL_CHAR_BUDGET": {"category": "tools", "type": "integer"},
        "USE_BUILTIN_RIPGREP": {"category": "tools", "type": "boolean"},
        # Configuration (general)
        "CLAUDE_CONFIG_DIR": {"category": "configuration", "type": None},
    }
