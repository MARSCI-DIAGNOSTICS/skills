#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
validate_schema.py - Validate Claude Code settings JSON schema

Standalone validator for the custom settings schema.

Usage:
    python validate_schema.py
    python validate_schema.py --verbose
    python validate_schema.py --check-examples

Dependencies:
    pip install jsonschema
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Any


def get_schema_path() -> Path:
    """Get path to the schema file."""
    script_dir = Path(__file__).resolve().parent
    return script_dir.parent.parent / "references" / "claude-code-settings.schema.json"


def load_schema(path: Path) -> dict[str, Any]:
    """Load and parse the JSON schema file."""
    if not path.exists():
        raise FileNotFoundError(f"Schema file not found: {path}")

    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def validate_draft07(schema: dict[str, Any]) -> tuple[bool, list[str]]:
    """Validate schema against JSON Schema draft-07."""
    errors = []

    try:
        from jsonschema import Draft7Validator
    except ImportError:
        return False, ["jsonschema package not installed. Run: pip install jsonschema"]

    try:
        Draft7Validator.check_schema(schema)
    except Exception as e:
        errors.append(f"Invalid JSON Schema: {e}")

    return len(errors) == 0, errors


def check_custom_metadata(schema: dict[str, Any]) -> list[str]:
    """Check custom x- metadata fields."""
    warnings = []

    # Required metadata
    required = {
        "x-schema-version": r"^\d+\.\d+\.\d+$",
        "x-claude-code-version": r"^\d+\.\d+\.\d+$",
        "x-last-updated": r"^\d{4}-\d{2}-\d{2}$",
    }

    import re
    for field, pattern in required.items():
        value = schema.get(field)
        if value is None:
            warnings.append(f"Missing required metadata: {field}")
        elif not re.match(pattern, str(value)):
            warnings.append(f"Invalid format for {field}: {value}")

    return warnings


def check_property_metadata(schema: dict[str, Any], verbose: bool = False) -> list[str]:
    """Check that properties have source annotations."""
    warnings = []
    properties = schema.get("properties", {})

    changelog_props = []
    official_props = []
    web_props = []
    unknown_props = []

    for name, definition in properties.items():
        source = definition.get("x-source")
        if source == "changelog":
            changelog_props.append(name)
        elif source == "official":
            official_props.append(name)
        elif source == "web":
            web_props.append(name)
        else:
            unknown_props.append(name)

    if verbose:
        print(f"\nProperty Sources:")
        print(f"  Official: {len(official_props)}")
        print(f"  Changelog: {len(changelog_props)}")
        print(f"  Web: {len(web_props)}")
        print(f"  Unknown: {len(unknown_props)}")

    if unknown_props:
        warnings.append(f"{len(unknown_props)} properties missing x-source: {', '.join(unknown_props[:5])}")

    return warnings


def check_examples(schema: dict[str, Any]) -> list[str]:
    """Validate that examples conform to schema."""
    errors = []

    try:
        from jsonschema import validate, ValidationError
    except ImportError:
        return ["jsonschema package not installed"]

    properties = schema.get("properties", {})
    for name, definition in properties.items():
        examples = definition.get("examples", [])
        prop_type = definition.get("type")

        for i, example in enumerate(examples):
            # Create a mini-schema for this property
            prop_schema = {"type": prop_type} if prop_type else {}
            if "enum" in definition:
                prop_schema["enum"] = definition["enum"]

            try:
                validate(instance=example, schema=prop_schema)
            except ValidationError as e:
                errors.append(f"{name} example[{i}]: {e.message}")

    return errors


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Validate Claude Code settings JSON schema"
    )
    parser.add_argument(
        "--verbose", "-v",
        action="store_true",
        help="Show detailed output"
    )
    parser.add_argument(
        "--check-examples",
        action="store_true",
        help="Also validate examples in properties"
    )
    parser.add_argument(
        "--schema",
        type=str,
        help="Path to schema file (default: auto-detect)"
    )

    args = parser.parse_args()

    # Load schema
    schema_path = Path(args.schema) if args.schema else get_schema_path()
    print(f"Validating: {schema_path}")

    try:
        schema = load_schema(schema_path)
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        return 1
    except json.JSONDecodeError as e:
        print(f"ERROR: Invalid JSON: {e}")
        return 1

    all_errors = []
    all_warnings = []

    # Validate draft-07
    is_valid, errors = validate_draft07(schema)
    if not is_valid:
        all_errors.extend(errors)
    elif args.verbose:
        print("  Draft-07 validation: PASS")

    # Check custom metadata
    warnings = check_custom_metadata(schema)
    all_warnings.extend(warnings)
    if args.verbose and not warnings:
        print("  Custom metadata: PASS")

    # Check property metadata
    warnings = check_property_metadata(schema, args.verbose)
    all_warnings.extend(warnings)

    # Check examples
    if args.check_examples:
        errors = check_examples(schema)
        all_errors.extend(errors)
        if args.verbose and not errors:
            print("  Examples validation: PASS")

    # Report results
    print()
    if all_errors:
        print(f"ERRORS ({len(all_errors)}):")
        for error in all_errors:
            print(f"  - {error}")

    if all_warnings:
        print(f"WARNINGS ({len(all_warnings)}):")
        for warning in all_warnings:
            print(f"  - {warning}")

    if not all_errors and not all_warnings:
        print("Schema is valid")
        print(f"  Version: {schema.get('x-schema-version')}")
        print(f"  Claude Code: {schema.get('x-claude-code-version')}")
        print(f"  Properties: {len(schema.get('properties', {}))}")
        print(f"  Last Updated: {schema.get('x-last-updated')}")
        return 0
    elif all_errors:
        return 1
    else:
        print("\nValidation passed with warnings")
        return 0


if __name__ == "__main__":
    sys.exit(main())
