#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
generate_schema.py - Generate and update Claude Code settings JSON schema

This script generates an extended JSON schema for Claude Code settings by:
1. Starting from the current schema as base
2. Extracting environment variables from canonical docs (via extract_env_vars.py)
3. Merging changelog-discovered settings
4. Adding custom metadata (x-since, x-source)
5. Validating the result as valid JSON Schema draft-07

Usage:
    python generate_schema.py --validate-only
    python generate_schema.py --dry-run
    python generate_schema.py --diff
    python generate_schema.py --sync-env-vars  # Update env vars from canonical docs
    python generate_schema.py  # Full update

Dependencies:
    pip install jsonschema requests pyyaml
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def get_script_dir() -> Path:
    """Get the directory containing this script."""
    return Path(__file__).resolve().parent


def get_schema_path() -> Path:
    """Get path to the schema file."""
    return get_script_dir().parent.parent / "references" / "claude-code-settings.schema.json"


def load_schema(path: Path) -> dict[str, Any]:
    """Load and parse the JSON schema file."""
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def save_schema(path: Path, schema: dict[str, Any]) -> None:
    """Save schema to file with proper formatting."""
    with open(path, "w", encoding="utf-8") as f:
        json.dump(schema, f, indent=2, ensure_ascii=False)
        f.write("\n")  # Trailing newline


def validate_schema(schema: dict[str, Any]) -> tuple[bool, list[str]]:
    """
    Validate that the schema is valid JSON Schema draft-07.

    Returns:
        Tuple of (is_valid, list of error messages)
    """
    errors = []

    try:
        from jsonschema import Draft7Validator, SchemaError
    except ImportError:
        return False, ["jsonschema package not installed. Run: pip install jsonschema"]

    # Check basic structure
    if "$schema" not in schema:
        errors.append("Missing $schema field")
    elif "draft-07" not in schema.get("$schema", ""):
        errors.append(f"Expected draft-07 schema, got: {schema.get('$schema')}")

    if schema.get("type") != "object":
        errors.append("Root type must be 'object'")

    if "properties" not in schema:
        errors.append("Missing 'properties' field")

    # Validate using jsonschema
    try:
        Draft7Validator.check_schema(schema)
    except SchemaError as e:
        errors.append(f"Invalid JSON Schema: {e.message}")

    # Check custom metadata
    required_meta = ["x-schema-version", "x-claude-code-version", "x-last-updated"]
    for field in required_meta:
        if field not in schema:
            errors.append(f"Missing custom metadata field: {field}")

    return len(errors) == 0, errors


def parse_changelog_settings(changelog_text: str) -> dict[str, dict[str, Any]]:
    """
    Parse changelog text to extract settings-related changes.

    Returns:
        Dict mapping setting names to metadata (version, description, source)
    """
    settings = {}

    # Patterns to match settings mentions in changelog
    patterns = [
        # "Added `settingName` setting" or "Added `settingName` - description"
        r"[Aa]dded\s+`([a-zA-Z_][a-zA-Z0-9_]*)`\s+(?:setting)?[^`]*?(?:[-–—]\s*)?([^\n]+)?",
        # "New setting: settingName"
        r"[Nn]ew\s+setting[:\s]+`?([a-zA-Z_][a-zA-Z0-9_]*)`?",
        # Environment variables
        r"[Aa]dded\s+`?(CLAUDE_[A-Z_]+|ANTHROPIC_[A-Z_]+)`?\s+(?:environment\s+variable)?",
    ]

    # Extract version headers
    version_pattern = r"##\s*\[?v?(\d+\.\d+\.\d+)\]?"
    current_version = None

    for line in changelog_text.split("\n"):
        # Check for version header
        version_match = re.search(version_pattern, line)
        if version_match:
            current_version = version_match.group(1)
            continue

        if not current_version:
            continue

        # Check for setting patterns
        for pattern in patterns:
            match = re.search(pattern, line)
            if match:
                setting_name = match.group(1)
                description = match.group(2) if len(match.groups()) > 1 else None

                if setting_name not in settings:
                    settings[setting_name] = {
                        "version": current_version,
                        "description": description.strip() if description else None,
                        "source": "changelog"
                    }

    return settings


def compute_changelog_hash(changelog_text: str) -> str:
    """Compute SHA256 hash of changelog content."""
    return f"sha256:{hashlib.sha256(changelog_text.encode('utf-8')).hexdigest()}"


def merge_sources(
    base_schema: dict[str, Any],
    changelog_settings: dict[str, dict[str, Any]],
    web_settings: dict[str, dict[str, Any]] | None = None
) -> tuple[dict[str, Any], list[str]]:
    """
    Merge settings from multiple sources with priority: official > web > changelog.

    Args:
        base_schema: Current schema to update
        changelog_settings: Settings discovered from changelog
        web_settings: Settings discovered from web search (optional)

    Returns:
        Updated schema with merged settings
    """
    schema = json.loads(json.dumps(base_schema))  # Deep copy
    properties = schema.get("properties", {})

    # Track what was added
    added = []

    # Merge changelog settings
    for name, meta in changelog_settings.items():
        if name not in properties:
            # Add new property with basic type inference
            properties[name] = {
                "type": "string",  # Default, may need refinement
                "description": meta.get("description", f"Added in v{meta['version']}"),
                "x-since": meta["version"],
                "x-source": "changelog"
            }
            added.append(f"{name} (v{meta['version']})")
        else:
            # Update existing property with version info if missing
            if "x-since" not in properties[name]:
                properties[name]["x-since"] = meta["version"]
            if "x-source" not in properties[name]:
                properties[name]["x-source"] = "changelog"

    # Merge web settings (higher priority than changelog)
    if web_settings:
        for name, meta in web_settings.items():
            if name in properties:
                # Web source overrides changelog for description
                if meta.get("description") and properties[name].get("x-source") == "changelog":
                    properties[name]["description"] = meta["description"]
                    properties[name]["x-source"] = "web"

    schema["properties"] = properties

    return schema, added


def update_metadata(
    schema: dict[str, Any],
    claude_code_version: str,
    changelog_hash: str
) -> dict[str, Any]:
    """Update schema metadata fields."""
    schema["x-last-updated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    schema["x-claude-code-version"] = claude_code_version
    schema["x-changelog-hash"] = changelog_hash

    # Increment patch version
    current_version = schema.get("x-schema-version", "1.0.0")
    parts = current_version.split(".")
    parts[-1] = str(int(parts[-1]) + 1)
    schema["x-schema-version"] = ".".join(parts)

    return schema


def diff_schemas(old_schema: dict[str, Any], new_schema: dict[str, Any]) -> list[str]:
    """Generate a diff between two schemas."""
    diffs = []

    old_props = set(old_schema.get("properties", {}).keys())
    new_props = set(new_schema.get("properties", {}).keys())

    added = new_props - old_props
    removed = old_props - new_props

    if added:
        diffs.append(f"+ Added properties: {', '.join(sorted(added))}")
    if removed:
        diffs.append(f"- Removed properties: {', '.join(sorted(removed))}")

    # Check for modified properties
    for prop in old_props & new_props:
        old_def = old_schema["properties"][prop]
        new_def = new_schema["properties"][prop]
        if old_def != new_def:
            diffs.append(f"~ Modified: {prop}")

    # Check env var changes
    old_env = old_schema.get("properties", {}).get("env", {}).get("properties", {})
    new_env = new_schema.get("properties", {}).get("env", {}).get("properties", {})
    old_env_keys = set(old_env.keys())
    new_env_keys = set(new_env.keys())

    env_added = new_env_keys - old_env_keys
    env_removed = old_env_keys - new_env_keys

    if env_added:
        diffs.append(f"+ Added env vars: {', '.join(sorted(env_added))}")
    if env_removed:
        diffs.append(f"- Removed env vars: {', '.join(sorted(env_removed))}")

    # Check metadata changes
    meta_fields = ["x-schema-version", "x-claude-code-version", "x-last-updated", "x-env-var-count"]
    for field in meta_fields:
        old_val = old_schema.get(field)
        new_val = new_schema.get(field)
        if old_val != new_val:
            diffs.append(f"  {field}: {old_val} -> {new_val}")

    return diffs


def get_canonical_docs_path() -> Path:
    """Get path to canonical settings.md from docs-management."""
    return (
        get_script_dir().parent.parent.parent
        / "docs-management"
        / "canonical"
        / "code-claude-com"
        / "docs"
        / "en"
        / "settings.md"
    )


def extract_env_vars_from_docs() -> dict[str, dict[str, Any]]:
    """
    Extract environment variables from canonical documentation.

    Uses extract_env_vars.py script to parse settings.md.

    Returns:
        Dict of env var definitions suitable for schema env.properties
    """
    extract_script = get_script_dir() / "extract_env_vars.py"
    docs_path = get_canonical_docs_path()

    if not extract_script.exists():
        print(f"Warning: extract_env_vars.py not found at {extract_script}", file=sys.stderr)
        return {}

    if not docs_path.exists():
        print(f"Warning: Canonical settings.md not found at {docs_path}", file=sys.stderr)
        return {}

    try:
        result = subprocess.run(
            [sys.executable, str(extract_script), "--docs-path", str(docs_path), "--quiet"],
            capture_output=True,
            text=True,
            check=True
        )
        return json.loads(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error running extract_env_vars.py: {e.stderr}", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing extract_env_vars.py output: {e}", file=sys.stderr)
        return {}


def sync_env_vars(schema: dict[str, Any], env_vars: dict[str, dict[str, Any]]) -> tuple[dict[str, Any], list[str]]:
    """
    Synchronize environment variables in schema with extracted vars.

    Args:
        schema: Current schema
        env_vars: Extracted env var definitions

    Returns:
        Updated schema and list of changes made
    """
    schema = json.loads(json.dumps(schema))  # Deep copy
    changes = []

    # Get or create env.properties
    if "properties" not in schema:
        schema["properties"] = {}
    if "env" not in schema["properties"]:
        schema["properties"]["env"] = {"type": "object", "properties": {}}
    if "properties" not in schema["properties"]["env"]:
        schema["properties"]["env"]["properties"] = {}

    current_env = schema["properties"]["env"]["properties"]

    # Track what we changed
    added = []
    updated = []

    for var_name, var_def in env_vars.items():
        if var_name not in current_env:
            current_env[var_name] = var_def
            added.append(var_name)
        else:
            # Update if definition differs (official docs take priority)
            if var_def.get("x-source") == "official":
                # Only update if we have more info (e.g., better description)
                if var_def.get("description") and var_def["description"] != current_env[var_name].get("description"):
                    current_env[var_name]["description"] = var_def["description"]
                    updated.append(var_name)
                # Add missing metadata
                for key in ["x-category", "x-since", "deprecated"]:
                    if key in var_def and key not in current_env[var_name]:
                        current_env[var_name][key] = var_def[key]
                        if var_name not in updated:
                            updated.append(var_name)

    # Update env var count
    schema["properties"]["env"]["x-env-var-count"] = len(current_env)
    schema["x-env-var-count"] = len(current_env)

    if added:
        changes.append(f"Added {len(added)} env vars: {', '.join(sorted(added)[:5])}")
        if len(added) > 5:
            changes.append(f"  ... and {len(added) - 5} more")
    if updated:
        changes.append(f"Updated {len(updated)} env vars")

    return schema, changes


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate and update Claude Code settings JSON schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Validate current schema without changes
  python generate_schema.py --validate-only

  # Show what would change without writing
  python generate_schema.py --dry-run

  # Show diff between current and new
  python generate_schema.py --diff

  # Full update (read, merge, validate, write)
  python generate_schema.py
        """
    )

    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Validate current schema without updating"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show changes without writing"
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="Show diff between current and generated"
    )
    parser.add_argument(
        "--changelog",
        type=str,
        help="Path to CHANGELOG.md file (optional, will fetch from GitHub if not provided)"
    )
    parser.add_argument(
        "--version",
        type=str,
        default="2.1.9",
        help="Claude Code version being tracked"
    )
    parser.add_argument(
        "--sync-env-vars",
        action="store_true",
        help="Sync environment variables from canonical docs (docs-management)"
    )

    args = parser.parse_args()

    schema_path = get_schema_path()
    print(f"Schema path: {schema_path}")

    # Load current schema
    try:
        current_schema = load_schema(schema_path)
        print(f"Loaded schema v{current_schema.get('x-schema-version', 'unknown')}")
    except FileNotFoundError:
        print("Schema file not found, will create new")
        current_schema = None

    # Validate only mode
    if args.validate_only:
        if current_schema is None:
            print("ERROR: No schema to validate")
            return 1

        is_valid, errors = validate_schema(current_schema)
        if is_valid:
            print("Schema is valid JSON Schema draft-07")
            print(f"  Properties: {len(current_schema.get('properties', {}))}")
            print(f"  Version: {current_schema.get('x-schema-version')}")
            print(f"  Claude Code: {current_schema.get('x-claude-code-version')}")
            return 0
        else:
            print("Schema validation FAILED:")
            for error in errors:
                print(f"  - {error}")
            return 1

    # Sync env vars from canonical docs if requested or during full update
    env_var_changes = []
    if args.sync_env_vars or not (args.validate_only or args.diff):
        print("Extracting environment variables from canonical docs...")
        env_vars = extract_env_vars_from_docs()
        if env_vars:
            print(f"Found {len(env_vars)} env vars in canonical docs")
            if current_schema:
                current_schema, env_var_changes = sync_env_vars(current_schema, env_vars)
                for change in env_var_changes:
                    print(f"  {change}")
        else:
            print("  No env vars extracted (check if canonical docs exist)")

    # For full update, we need changelog
    changelog_text = ""
    changelog_hash = ""

    if args.changelog:
        changelog_path = Path(args.changelog)
        if changelog_path.exists():
            changelog_text = changelog_path.read_text(encoding="utf-8")
            changelog_hash = compute_changelog_hash(changelog_text)

    # Parse changelog if available
    changelog_settings = {}
    if changelog_text:
        changelog_settings = parse_changelog_settings(changelog_text)
        print(f"Found {len(changelog_settings)} settings in changelog")

    # Generate updated schema
    if current_schema:
        new_schema, added = merge_sources(current_schema, changelog_settings)
        new_schema = update_metadata(new_schema, args.version, changelog_hash or current_schema.get("x-changelog-hash", ""))

        if added:
            print(f"Added {len(added)} new properties:")
            for prop in added[:10]:
                print(f"  + {prop}")
            if len(added) > 10:
                print(f"  ... and {len(added) - 10} more")
    else:
        print("ERROR: Cannot generate without existing schema")
        return 1

    # Validate new schema
    is_valid, errors = validate_schema(new_schema)
    if not is_valid:
        print("Generated schema is invalid:")
        for error in errors:
            print(f"  - {error}")
        return 1

    print("Generated schema is valid")

    # Diff mode
    if args.diff:
        diffs = diff_schemas(current_schema, new_schema)
        if diffs:
            print("\nChanges:")
            for diff in diffs:
                print(f"  {diff}")
        else:
            print("\nNo changes detected")
        return 0

    # Dry run mode
    if args.dry_run:
        print("\n[DRY RUN] Would write schema with:")
        print(f"  Version: {new_schema.get('x-schema-version')}")
        print(f"  Properties: {len(new_schema.get('properties', {}))}")
        print(f"  Updated: {new_schema.get('x-last-updated')}")
        return 0

    # Write updated schema
    save_schema(schema_path, new_schema)
    env_count = len(new_schema.get("properties", {}).get("env", {}).get("properties", {}))
    print(f"\nSchema updated: {schema_path}")
    print(f"  Version: {new_schema.get('x-schema-version')}")
    print(f"  Properties: {len(new_schema.get('properties', {}))}")
    print(f"  Environment Variables: {env_count}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
