#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_env_vars.py - Extract environment variables from Claude Code documentation

This script extracts environment variable definitions from:
1. Canonical settings.md from docs-management
2. CHANGELOG.md for undocumented discoveries

Output format is JSON suitable for merging into the schema's env.properties.

SINGLE SOURCE OF TRUTH: Categories and types are inferred from naming patterns,
NOT hardcoded per-variable. This ensures new env vars work without code changes.

Usage:
    python extract_env_vars.py --docs-path /path/to/settings.md
    python extract_env_vars.py --docs-path /path/to/settings.md --changelog /path/to/CHANGELOG.md
    python extract_env_vars.py --output json  # (default)
    python extract_env_vars.py --output yaml

Dependencies:
    pip install pyyaml  # optional, for YAML output
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any


# =============================================================================
# PATTERN-BASED INFERENCE (Single Source of Truth)
# =============================================================================
# Categories and types are derived from naming conventions, not hardcoded per-variable.
# When Claude Code adds new env vars following their naming conventions, they
# automatically get correct categories and type metadata.

# Category inference patterns (order matters - first match wins)
# Each pattern is (regex, category) - regex is matched against the full var name
CATEGORY_PATTERNS: list[tuple[str, str]] = [
    # Authentication - keys, tokens, auth headers
    (r"^ANTHROPIC_API_KEY$", "authentication"),
    (r"^ANTHROPIC_AUTH", "authentication"),
    (r"^ANTHROPIC_CUSTOM_HEADERS$", "authentication"),
    (r"^ANTHROPIC_FOUNDRY_API_KEY$", "authentication"),
    (r"^AWS_.*TOKEN", "authentication"),

    # Model configuration - model selection and defaults
    (r"^ANTHROPIC_MODEL$", "model-config"),
    (r"^ANTHROPIC_DEFAULT_", "model-config"),
    (r"^ANTHROPIC_SMALL_FAST_MODEL", "model-config"),
    (r"^CLAUDE_CODE_SUBAGENT_MODEL$", "model-config"),

    # Provider selection - which LLM backend to use
    (r"^CLAUDE_CODE_USE_", "provider"),
    (r"^CLAUDE_CODE_SKIP_.*AUTH$", "provider"),

    # Bash behavior - shell execution settings
    (r"^BASH_", "bash-behavior"),
    (r"^CLAUDE_BASH_", "bash-behavior"),
    (r"^CLAUDE_CODE_SHELL", "bash-behavior"),
    (r"^CLAUDE_ENV_FILE$", "bash-behavior"),

    # Disable flags - feature toggles
    (r"^DISABLE_", "disable-flags"),
    (r"^CLAUDE_CODE_DISABLE_", "disable-flags"),

    # Proxy settings
    (r"^HTTPS?_PROXY$", "proxy"),
    (r"^NO_PROXY$", "proxy"),

    # MCP (Model Context Protocol) settings
    (r"^MCP_", "mcp"),
    (r"^MAX_MCP_", "mcp"),
    (r"^ENABLE_TOOL_", "mcp"),
    (r"^MAX_THINKING_", "mcp"),

    # Vertex AI and Bedrock region overrides
    (r"^VERTEX_REGION_", "vertex-bedrock"),

    # Tools configuration
    (r"^SLASH_COMMAND_", "tools"),
    (r"^USE_BUILTIN_", "tools"),

    # General configuration (broad patterns - should be last)
    (r"^CLAUDE_CODE_", "configuration"),
    (r"^CLAUDE_CONFIG_", "configuration"),
    (r"^CLAUDE_SESSION_", "configuration"),
]

# Type inference patterns for detecting boolean flags and integer values
# These help generate correct enum/x-value-type metadata
TYPE_INFERENCE_PATTERNS: dict[str, list[str]] = {
    # Boolean flags (typically 0/1 values)
    "boolean": [
        r"^DISABLE_",           # DISABLE_TELEMETRY, DISABLE_AUTOUPDATER
        r"_DISABLE_",           # CLAUDE_CODE_DISABLE_TERMINAL_TITLE
        r"_SKIP_",              # CLAUDE_CODE_SKIP_VERTEX_AUTH
        r"_HIDE_",              # CLAUDE_CODE_HIDE_ACCOUNT_INFO
        r"^CLAUDE_CODE_USE_",   # CLAUDE_CODE_USE_BEDROCK
        r"^USE_BUILTIN_",       # USE_BUILTIN_RIPGREP
    ],
    # Integer values (timeouts, token limits, sizes)
    "integer": [
        r"_TIMEOUT",            # MCP_TIMEOUT, MCP_TOOL_TIMEOUT
        r"_MS$",                # BASH_DEFAULT_TIMEOUT_MS
        r"_TOKENS$",            # MAX_THINKING_TOKENS, MAX_MCP_OUTPUT_TOKENS
        r"_LENGTH$",            # BASH_MAX_OUTPUT_LENGTH
        r"_BUDGET$",            # SLASH_COMMAND_TOOL_CHAR_BUDGET
        r"_TTL_MS$",            # CLAUDE_CODE_API_KEY_HELPER_TTL_MS
        r"_DEBOUNCE_MS$",       # CLAUDE_CODE_OTEL_HEADERS_HELPER_DEBOUNCE_MS
    ],
}


def infer_category(var_name: str) -> str:
    """
    Infer category from variable name using pattern matching.

    Args:
        var_name: Environment variable name (e.g., "ANTHROPIC_API_KEY")

    Returns:
        Category string (e.g., "authentication") or "uncategorized" if no match
    """
    for pattern, category in CATEGORY_PATTERNS:
        if re.match(pattern, var_name):
            return category
    return "uncategorized"


def infer_type_metadata(var_name: str, description: str = "") -> dict[str, Any]:
    """
    Infer type metadata from variable name and description.

    Args:
        var_name: Environment variable name
        description: Variable description (for additional hints)

    Returns:
        Dict with type metadata (enum for booleans, x-value-type for integers)
    """
    metadata: dict[str, Any] = {}

    # Check for boolean patterns
    for pattern in TYPE_INFERENCE_PATTERNS["boolean"]:
        if re.search(pattern, var_name):
            metadata["enum"] = ["0", "1"]
            break

    # Check for integer patterns
    if "enum" not in metadata:  # Don't add x-value-type if already a boolean
        for pattern in TYPE_INFERENCE_PATTERNS["integer"]:
            if re.search(pattern, var_name):
                metadata["x-value-type"] = "integer"
                break

    return metadata


def get_script_dir() -> Path:
    """Get the directory containing this script."""
    return Path(__file__).resolve().parent


def get_default_docs_path() -> Path:
    """Get default path to canonical settings.md."""
    # Path from scripts/schema/ to skills/docs-management/canonical/...
    return (
        get_script_dir().parent.parent.parent
        / "docs-management"
        / "canonical"
        / "code-claude-com"
        / "docs"
        / "en"
        / "settings.md"
    )


def extract_env_vars_from_settings_md(content: str) -> dict[str, dict[str, Any]]:
    """
    Extract environment variables from settings.md markdown table.

    Expected format:
    | `VARIABLE_NAME` | Description text |

    Returns:
        Dict mapping variable names to their properties
    """
    env_vars = {}

    # Pattern to match markdown table rows with env var definitions
    # Format: | `VAR_NAME` | Description |
    table_pattern = re.compile(
        r"^\|\s*`([A-Z][A-Z0-9_]+)`\s*\|\s*(.+?)\s*\|?\s*$",
        re.MULTILINE
    )

    for match in table_pattern.finditer(content):
        var_name = match.group(1).strip()
        description = match.group(2).strip()

        # Clean up description - remove markdown formatting
        description = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", description)  # [text](url) -> text
        description = re.sub(r"`([^`]+)`", r"\1", description)  # `code` -> code
        description = re.sub(r"\*\*([^*]+)\*\*", r"\1", description)  # **bold** -> bold
        description = description.replace("\\", "")  # Remove escape chars

        # Build property definition
        prop_def: dict[str, Any] = {
            "type": "string",
            "description": description,
            "x-source": "official",
        }

        # Add category using pattern inference
        category = infer_category(var_name)
        if category != "uncategorized":
            prop_def["x-category"] = category

        # Add type metadata using pattern inference
        type_metadata = infer_type_metadata(var_name, description)
        prop_def.update(type_metadata)

        # Check for deprecated
        if "[DEPRECATED]" in description or "DEPRECATED" in description:
            prop_def["deprecated"] = True
            prop_def["x-deprecation-note"] = "See description for migration guidance"

        env_vars[var_name] = prop_def

    return env_vars


def extract_env_vars_from_changelog(content: str) -> dict[str, dict[str, Any]]:
    """
    Extract environment variables discovered in CHANGELOG.md.

    These are often announced before appearing in official docs.

    Returns:
        Dict mapping variable names to their properties (with x-source: "changelog")
    """
    env_vars = {}

    # Pattern for env var announcements in changelog
    # Examples: "Added `CLAUDE_CODE_TMPDIR`", "New environment variable `VAR_NAME`"
    patterns = [
        r"[Aa]dded\s+`(CLAUDE_[A-Z0-9_]+)`",
        r"[Aa]dded\s+`(ANTHROPIC_[A-Z0-9_]+)`",
        r"[Aa]dded\s+`(DISABLE_[A-Z0-9_]+)`",
        r"[Nn]ew\s+(?:environment\s+)?variable[:\s]+`?([A-Z][A-Z0-9_]+)`?",
        r"`([A-Z][A-Z0-9_]+)`\s+environment\s+variable",
    ]

    # Extract version headers
    version_pattern = re.compile(r"##\s*\[?v?(\d+\.\d+\.\d+)\]?")
    current_version = None

    for line in content.split("\n"):
        # Check for version header
        version_match = version_pattern.search(line)
        if version_match:
            current_version = version_match.group(1)
            continue

        if not current_version:
            continue

        # Check for env var patterns
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                var_name = match.group(1)

                # Skip if already found (prefer earlier/first mention)
                if var_name in env_vars:
                    continue

                # Build property definition
                prop_def: dict[str, Any] = {
                    "type": "string",
                    "description": f"Added in v{current_version}",
                    "x-source": "changelog",
                    "x-since": current_version,
                }

                # Add category using pattern inference
                category = infer_category(var_name)
                if category != "uncategorized":
                    prop_def["x-category"] = category

                # Add type metadata using pattern inference
                type_metadata = infer_type_metadata(var_name)
                prop_def.update(type_metadata)

                env_vars[var_name] = prop_def

    return env_vars


def merge_env_vars(
    official: dict[str, dict[str, Any]],
    changelog: dict[str, dict[str, Any]]
) -> dict[str, dict[str, Any]]:
    """
    Merge env vars from multiple sources. Official takes precedence.

    Args:
        official: Env vars from settings.md (x-source: "official")
        changelog: Env vars from CHANGELOG.md (x-source: "changelog")

    Returns:
        Merged dict with official overriding changelog for duplicates
    """
    merged = {}

    # Add changelog entries first (lower priority)
    for name, props in changelog.items():
        merged[name] = props

    # Add/override with official entries (higher priority)
    for name, props in official.items():
        if name in merged:
            # Preserve x-since from changelog if official doesn't have it
            if "x-since" not in props and "x-since" in merged[name]:
                props["x-since"] = merged[name]["x-since"]
        merged[name] = props

    return merged


def format_output(env_vars: dict[str, dict[str, Any]], format_type: str) -> str:
    """Format output as JSON or YAML."""
    # Sort by name for consistent output
    sorted_vars = dict(sorted(env_vars.items()))

    if format_type == "yaml":
        try:
            import yaml
            return yaml.dump(sorted_vars, default_flow_style=False, sort_keys=False)
        except ImportError:
            print("Warning: PyYAML not installed, falling back to JSON", file=sys.stderr)
            format_type = "json"

    return json.dumps(sorted_vars, indent=2, ensure_ascii=False)


def print_summary(env_vars: dict[str, dict[str, Any]]) -> None:
    """Print summary statistics to stderr."""
    total = len(env_vars)
    official = sum(1 for v in env_vars.values() if v.get("x-source") == "official")
    changelog = sum(1 for v in env_vars.values() if v.get("x-source") == "changelog")
    deprecated = sum(1 for v in env_vars.values() if v.get("deprecated"))

    # Count by category
    categories: dict[str, int] = {}
    for props in env_vars.values():
        cat = props.get("x-category", "uncategorized")
        categories[cat] = categories.get(cat, 0) + 1

    # Count by type
    boolean_count = sum(1 for v in env_vars.values() if "enum" in v)
    integer_count = sum(1 for v in env_vars.values() if v.get("x-value-type") == "integer")

    print(f"\nEnvironment Variables Extracted: {total}", file=sys.stderr)
    print(f"  - Official (settings.md): {official}", file=sys.stderr)
    print(f"  - Changelog-discovered: {changelog}", file=sys.stderr)
    print(f"  - Deprecated: {deprecated}", file=sys.stderr)
    print(f"\nBy Type:", file=sys.stderr)
    print(f"  - Boolean (enum 0/1): {boolean_count}", file=sys.stderr)
    print(f"  - Integer (x-value-type): {integer_count}", file=sys.stderr)
    print(f"  - String (default): {total - boolean_count - integer_count}", file=sys.stderr)
    print("\nBy Category:", file=sys.stderr)
    for cat, count in sorted(categories.items()):
        print(f"  - {cat}: {count}", file=sys.stderr)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Extract environment variables from Claude Code documentation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Extract from canonical settings.md
  python extract_env_vars.py --docs-path /path/to/settings.md

  # Include changelog discoveries
  python extract_env_vars.py --docs-path /path/to/settings.md --changelog /path/to/CHANGELOG.md

  # Output as YAML
  python extract_env_vars.py --docs-path /path/to/settings.md --output yaml

  # Use default paths (docs-management canonical storage)
  python extract_env_vars.py
        """
    )

    parser.add_argument(
        "--docs-path",
        type=str,
        help="Path to settings.md file (defaults to docs-management canonical storage)"
    )
    parser.add_argument(
        "--changelog",
        type=str,
        help="Path to CHANGELOG.md file (optional)"
    )
    parser.add_argument(
        "--output",
        type=str,
        choices=["json", "yaml"],
        default="json",
        help="Output format (default: json)"
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress summary output"
    )

    args = parser.parse_args()

    # Determine docs path
    if args.docs_path:
        docs_path = Path(args.docs_path)
    else:
        docs_path = get_default_docs_path()

    if not docs_path.exists():
        print(f"ERROR: Settings file not found: {docs_path}", file=sys.stderr)
        return 1

    # Extract from official docs
    print(f"Reading: {docs_path}", file=sys.stderr)
    settings_content = docs_path.read_text(encoding="utf-8")
    official_vars = extract_env_vars_from_settings_md(settings_content)

    # Extract from changelog if provided
    changelog_vars: dict[str, dict[str, Any]] = {}
    if args.changelog:
        changelog_path = Path(args.changelog)
        if changelog_path.exists():
            print(f"Reading: {changelog_path}", file=sys.stderr)
            changelog_content = changelog_path.read_text(encoding="utf-8")
            changelog_vars = extract_env_vars_from_changelog(changelog_content)

    # Merge sources
    merged_vars = merge_env_vars(official_vars, changelog_vars)

    # Print summary
    if not args.quiet:
        print_summary(merged_vars)

    # Output result
    print(format_output(merged_vars, args.output))

    return 0


if __name__ == "__main__":
    sys.exit(main())
