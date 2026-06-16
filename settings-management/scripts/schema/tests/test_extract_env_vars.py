# -*- coding: utf-8 -*-
"""
Tests for extract_env_vars.py pattern-based inference.

Tests validate that:
1. Category inference works correctly for all known patterns
2. Type inference (boolean/integer) works correctly
3. Future env vars following naming conventions auto-categorize
4. Extraction from settings.md works correctly
5. Extraction from CHANGELOG.md works correctly
"""

import pytest
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from extract_env_vars import (
    infer_category,
    infer_type_metadata,
    extract_env_vars_from_settings_md,
    extract_env_vars_from_changelog,
    merge_env_vars,
)


class TestCategoryInference:
    """Tests for infer_category() pattern matching."""

    def test_authentication_category(self):
        """Authentication-related env vars are correctly categorized."""
        assert infer_category("ANTHROPIC_API_KEY") == "authentication"
        assert infer_category("ANTHROPIC_AUTH_TOKEN") == "authentication"
        assert infer_category("ANTHROPIC_CUSTOM_HEADERS") == "authentication"
        assert infer_category("ANTHROPIC_FOUNDRY_API_KEY") == "authentication"
        assert infer_category("AWS_BEARER_TOKEN_BEDROCK") == "authentication"

    def test_model_config_category(self):
        """Model configuration env vars are correctly categorized."""
        assert infer_category("ANTHROPIC_MODEL") == "model-config"
        assert infer_category("ANTHROPIC_DEFAULT_HAIKU_MODEL") == "model-config"
        assert infer_category("ANTHROPIC_DEFAULT_OPUS_MODEL") == "model-config"
        assert infer_category("ANTHROPIC_DEFAULT_SONNET_MODEL") == "model-config"
        assert infer_category("ANTHROPIC_SMALL_FAST_MODEL") == "model-config"
        assert infer_category("CLAUDE_CODE_SUBAGENT_MODEL") == "model-config"

    def test_provider_category(self):
        """Provider selection env vars are correctly categorized."""
        assert infer_category("CLAUDE_CODE_USE_BEDROCK") == "provider"
        assert infer_category("CLAUDE_CODE_USE_VERTEX") == "provider"
        assert infer_category("CLAUDE_CODE_USE_FOUNDRY") == "provider"
        assert infer_category("CLAUDE_CODE_SKIP_BEDROCK_AUTH") == "provider"
        assert infer_category("CLAUDE_CODE_SKIP_VERTEX_AUTH") == "provider"
        assert infer_category("CLAUDE_CODE_SKIP_FOUNDRY_AUTH") == "provider"

    def test_bash_behavior_category(self):
        """Bash behavior env vars are correctly categorized."""
        assert infer_category("BASH_DEFAULT_TIMEOUT_MS") == "bash-behavior"
        assert infer_category("BASH_MAX_OUTPUT_LENGTH") == "bash-behavior"
        assert infer_category("BASH_MAX_TIMEOUT_MS") == "bash-behavior"
        assert infer_category("CLAUDE_BASH_MAINTAIN_PROJECT_WORKING_DIR") == "bash-behavior"
        assert infer_category("CLAUDE_ENV_FILE") == "bash-behavior"
        assert infer_category("CLAUDE_CODE_SHELL") == "bash-behavior"
        assert infer_category("CLAUDE_CODE_SHELL_PREFIX") == "bash-behavior"

    def test_disable_flags_category(self):
        """Disable flag env vars are correctly categorized."""
        assert infer_category("DISABLE_TELEMETRY") == "disable-flags"
        assert infer_category("DISABLE_AUTOUPDATER") == "disable-flags"
        assert infer_category("DISABLE_COST_WARNINGS") == "disable-flags"
        assert infer_category("CLAUDE_CODE_DISABLE_TERMINAL_TITLE") == "disable-flags"
        assert infer_category("CLAUDE_CODE_DISABLE_NONESSENTIAL_TRAFFIC") == "disable-flags"

    def test_proxy_category(self):
        """Proxy env vars are correctly categorized."""
        assert infer_category("HTTP_PROXY") == "proxy"
        assert infer_category("HTTPS_PROXY") == "proxy"
        assert infer_category("NO_PROXY") == "proxy"

    def test_mcp_category(self):
        """MCP-related env vars are correctly categorized."""
        assert infer_category("MCP_TIMEOUT") == "mcp"
        assert infer_category("MCP_TOOL_TIMEOUT") == "mcp"
        assert infer_category("MAX_MCP_OUTPUT_TOKENS") == "mcp"
        assert infer_category("MAX_THINKING_TOKENS") == "mcp"
        assert infer_category("ENABLE_TOOL_SEARCH") == "mcp"

    def test_vertex_bedrock_category(self):
        """Vertex/Bedrock region env vars are correctly categorized."""
        assert infer_category("VERTEX_REGION_CLAUDE_4_0_OPUS") == "vertex-bedrock"
        assert infer_category("VERTEX_REGION_CLAUDE_3_5_HAIKU") == "vertex-bedrock"
        assert infer_category("VERTEX_REGION_CLAUDE_4_0_SONNET") == "vertex-bedrock"

    def test_tools_category(self):
        """Tools configuration env vars are correctly categorized."""
        assert infer_category("SLASH_COMMAND_TOOL_CHAR_BUDGET") == "tools"
        assert infer_category("USE_BUILTIN_RIPGREP") == "tools"

    def test_configuration_category(self):
        """General configuration env vars are correctly categorized."""
        assert infer_category("CLAUDE_CONFIG_DIR") == "configuration"
        assert infer_category("CLAUDE_SESSION_ID") == "configuration"
        assert infer_category("CLAUDE_CODE_TMPDIR") == "configuration"
        assert infer_category("CLAUDE_CODE_MAX_OUTPUT_TOKENS") == "configuration"

    def test_uncategorized_fallback(self):
        """Unknown env vars return 'uncategorized'."""
        assert infer_category("UNKNOWN_VARIABLE") == "uncategorized"
        assert infer_category("RANDOM_ENV_VAR") == "uncategorized"


class TestTypeInference:
    """Tests for infer_type_metadata() pattern matching."""

    def test_boolean_type_disable_prefix(self):
        """DISABLE_ prefix vars are detected as boolean."""
        meta = infer_type_metadata("DISABLE_TELEMETRY")
        assert meta.get("enum") == ["0", "1"]

    def test_boolean_type_disable_infix(self):
        """_DISABLE_ infix vars are detected as boolean."""
        meta = infer_type_metadata("CLAUDE_CODE_DISABLE_TERMINAL_TITLE")
        assert meta.get("enum") == ["0", "1"]

    def test_boolean_type_skip_infix(self):
        """_SKIP_ infix vars are detected as boolean."""
        meta = infer_type_metadata("CLAUDE_CODE_SKIP_VERTEX_AUTH")
        assert meta.get("enum") == ["0", "1"]

    def test_boolean_type_hide_infix(self):
        """_HIDE_ infix vars are detected as boolean."""
        meta = infer_type_metadata("CLAUDE_CODE_HIDE_ACCOUNT_INFO")
        assert meta.get("enum") == ["0", "1"]

    def test_boolean_type_use_prefix(self):
        """CLAUDE_CODE_USE_ prefix vars are detected as boolean."""
        meta = infer_type_metadata("CLAUDE_CODE_USE_BEDROCK")
        assert meta.get("enum") == ["0", "1"]

    def test_boolean_type_use_builtin_prefix(self):
        """USE_BUILTIN_ prefix vars are detected as boolean."""
        meta = infer_type_metadata("USE_BUILTIN_RIPGREP")
        assert meta.get("enum") == ["0", "1"]

    def test_integer_type_timeout(self):
        """_TIMEOUT vars are detected as integer."""
        meta = infer_type_metadata("MCP_TIMEOUT")
        assert meta.get("x-value-type") == "integer"
        meta = infer_type_metadata("MCP_TOOL_TIMEOUT")
        assert meta.get("x-value-type") == "integer"

    def test_integer_type_ms_suffix(self):
        """_MS suffix vars are detected as integer."""
        meta = infer_type_metadata("BASH_DEFAULT_TIMEOUT_MS")
        assert meta.get("x-value-type") == "integer"
        meta = infer_type_metadata("CLAUDE_CODE_API_KEY_HELPER_TTL_MS")
        assert meta.get("x-value-type") == "integer"

    def test_integer_type_tokens_suffix(self):
        """_TOKENS suffix vars are detected as integer."""
        meta = infer_type_metadata("MAX_THINKING_TOKENS")
        assert meta.get("x-value-type") == "integer"
        meta = infer_type_metadata("MAX_MCP_OUTPUT_TOKENS")
        assert meta.get("x-value-type") == "integer"

    def test_integer_type_length_suffix(self):
        """_LENGTH suffix vars are detected as integer."""
        meta = infer_type_metadata("BASH_MAX_OUTPUT_LENGTH")
        assert meta.get("x-value-type") == "integer"

    def test_integer_type_budget_suffix(self):
        """_BUDGET suffix vars are detected as integer."""
        meta = infer_type_metadata("SLASH_COMMAND_TOOL_CHAR_BUDGET")
        assert meta.get("x-value-type") == "integer"

    def test_string_type_default(self):
        """Vars without type patterns return empty metadata (string default)."""
        meta = infer_type_metadata("ANTHROPIC_MODEL")
        assert "enum" not in meta
        assert "x-value-type" not in meta

    def test_boolean_takes_precedence_over_integer(self):
        """Boolean patterns take precedence (no x-value-type added for booleans)."""
        # A hypothetical var that matches both patterns
        # DISABLE_*_TIMEOUT_MS would match both, boolean should win
        meta = infer_type_metadata("DISABLE_SOMETHING")
        assert meta.get("enum") == ["0", "1"]
        assert "x-value-type" not in meta


class TestFutureEnvVarsAutoCategorize:
    """
    Tests that future env vars following naming conventions auto-categorize.

    This is the key benefit of pattern-based inference - new vars work
    without code changes.
    """

    def test_new_disable_flag_auto_categorizes(self):
        """New DISABLE_ vars auto-categorize as disable-flags."""
        assert infer_category("DISABLE_NEW_FEATURE") == "disable-flags"
        assert infer_category("DISABLE_FANCY_ANIMATION") == "disable-flags"
        meta = infer_type_metadata("DISABLE_NEW_FEATURE")
        assert meta.get("enum") == ["0", "1"]

    def test_new_claude_code_disable_auto_categorizes(self):
        """New CLAUDE_CODE_DISABLE_ vars auto-categorize."""
        assert infer_category("CLAUDE_CODE_DISABLE_NEW_THING") == "disable-flags"
        meta = infer_type_metadata("CLAUDE_CODE_DISABLE_NEW_THING")
        assert meta.get("enum") == ["0", "1"]

    def test_new_timeout_var_auto_categorizes(self):
        """New _TIMEOUT vars get integer type."""
        meta = infer_type_metadata("NEW_FEATURE_TIMEOUT")
        assert meta.get("x-value-type") == "integer"

    def test_new_ms_var_auto_categorizes(self):
        """New _MS suffix vars get integer type."""
        meta = infer_type_metadata("CLAUDE_CODE_NEW_TIMEOUT_MS")
        assert meta.get("x-value-type") == "integer"

    def test_new_tokens_var_auto_categorizes(self):
        """New _TOKENS suffix vars get integer type."""
        meta = infer_type_metadata("MAX_NEW_FEATURE_TOKENS")
        assert meta.get("x-value-type") == "integer"

    def test_new_use_var_auto_categorizes(self):
        """New CLAUDE_CODE_USE_ vars auto-categorize as provider + boolean."""
        assert infer_category("CLAUDE_CODE_USE_NEW_PROVIDER") == "provider"
        meta = infer_type_metadata("CLAUDE_CODE_USE_NEW_PROVIDER")
        assert meta.get("enum") == ["0", "1"]

    def test_new_vertex_region_auto_categorizes(self):
        """New VERTEX_REGION_ vars auto-categorize."""
        assert infer_category("VERTEX_REGION_CLAUDE_5_0_OPUS") == "vertex-bedrock"

    def test_new_anthropic_default_auto_categorizes(self):
        """New ANTHROPIC_DEFAULT_ vars auto-categorize as model-config."""
        assert infer_category("ANTHROPIC_DEFAULT_NEW_MODEL") == "model-config"

    def test_new_mcp_var_auto_categorizes(self):
        """New MCP_ vars auto-categorize."""
        assert infer_category("MCP_NEW_SETTING") == "mcp"


class TestExtractionFromSettingsMd:
    """Tests for extract_env_vars_from_settings_md()."""

    def test_extracts_basic_env_vars(self, sample_settings_md):
        """Extracts env vars from markdown table."""
        result = extract_env_vars_from_settings_md(sample_settings_md)

        assert "ANTHROPIC_API_KEY" in result
        assert "ANTHROPIC_MODEL" in result
        assert "DISABLE_TELEMETRY" in result

    def test_sets_correct_source(self, sample_settings_md):
        """All extracted vars have x-source: official."""
        result = extract_env_vars_from_settings_md(sample_settings_md)

        for props in result.values():
            assert props.get("x-source") == "official"

    def test_cleans_markdown_from_description(self, sample_settings_md):
        """Markdown formatting is removed from descriptions."""
        result = extract_env_vars_from_settings_md(sample_settings_md)

        # [Model Configuration](/docs/model-configuration) should become "Model Configuration"
        desc = result["ANTHROPIC_MODEL"]["description"]
        assert "[" not in desc
        assert "](/docs/" not in desc

    def test_detects_deprecated_flag(self, sample_settings_md):
        """Deprecated vars are marked correctly."""
        result = extract_env_vars_from_settings_md(sample_settings_md)

        assert result["ANTHROPIC_SMALL_FAST_MODEL"].get("deprecated") is True

    def test_applies_category_inference(self, sample_settings_md):
        """Categories are inferred correctly."""
        result = extract_env_vars_from_settings_md(sample_settings_md)

        assert result["ANTHROPIC_API_KEY"].get("x-category") == "authentication"
        assert result["ANTHROPIC_MODEL"].get("x-category") == "model-config"
        assert result["DISABLE_TELEMETRY"].get("x-category") == "disable-flags"

    def test_applies_type_inference(self, sample_settings_md):
        """Type metadata is inferred correctly."""
        result = extract_env_vars_from_settings_md(sample_settings_md)

        assert result["DISABLE_TELEMETRY"].get("enum") == ["0", "1"]
        assert result["BASH_DEFAULT_TIMEOUT_MS"].get("x-value-type") == "integer"
        assert result["CLAUDE_CODE_USE_BEDROCK"].get("enum") == ["0", "1"]


class TestExtractionFromChangelog:
    """Tests for extract_env_vars_from_changelog()."""

    def test_extracts_env_vars_from_changelog(self, sample_changelog_md):
        """Extracts env vars mentioned in changelog."""
        result = extract_env_vars_from_changelog(sample_changelog_md)

        assert "CLAUDE_CODE_TMPDIR" in result
        assert "CLAUDE_CODE_DISABLE_BACKGROUND_TASKS" in result
        assert "CLAUDE_SESSION_ID" in result

    def test_sets_changelog_source(self, sample_changelog_md):
        """All extracted vars have x-source: changelog."""
        result = extract_env_vars_from_changelog(sample_changelog_md)

        for props in result.values():
            assert props.get("x-source") == "changelog"

    def test_captures_version(self, sample_changelog_md):
        """Version is captured in x-since."""
        result = extract_env_vars_from_changelog(sample_changelog_md)

        assert result["CLAUDE_CODE_TMPDIR"].get("x-since") == "2.1.5"
        assert result["CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"].get("x-since") == "2.1.4"
        assert result["CLAUDE_SESSION_ID"].get("x-since") == "2.1.0"

    def test_applies_category_inference(self, sample_changelog_md):
        """Categories are inferred for changelog vars."""
        result = extract_env_vars_from_changelog(sample_changelog_md)

        assert result["CLAUDE_CODE_TMPDIR"].get("x-category") == "configuration"
        assert result["CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"].get("x-category") == "disable-flags"

    def test_applies_type_inference(self, sample_changelog_md):
        """Type metadata is inferred for changelog vars."""
        result = extract_env_vars_from_changelog(sample_changelog_md)

        assert result["CLAUDE_CODE_DISABLE_BACKGROUND_TASKS"].get("enum") == ["0", "1"]


class TestMergeEnvVars:
    """Tests for merge_env_vars()."""

    def test_official_takes_precedence(self):
        """Official entries override changelog entries."""
        official = {
            "VAR": {"description": "Official desc", "x-source": "official"}
        }
        changelog = {
            "VAR": {"description": "Changelog desc", "x-source": "changelog", "x-since": "2.0.0"}
        }

        result = merge_env_vars(official, changelog)

        assert result["VAR"]["description"] == "Official desc"
        assert result["VAR"]["x-source"] == "official"

    def test_preserves_x_since_from_changelog(self):
        """x-since is preserved from changelog when merging."""
        official = {
            "VAR": {"description": "Official desc", "x-source": "official"}
        }
        changelog = {
            "VAR": {"description": "Changelog desc", "x-source": "changelog", "x-since": "2.0.0"}
        }

        result = merge_env_vars(official, changelog)

        assert result["VAR"]["x-since"] == "2.0.0"

    def test_includes_changelog_only_vars(self):
        """Vars only in changelog are included."""
        official = {"VAR1": {"description": "Var 1"}}
        changelog = {"VAR2": {"description": "Var 2", "x-since": "2.0.0"}}

        result = merge_env_vars(official, changelog)

        assert "VAR1" in result
        assert "VAR2" in result


class TestKnownEnvVarsRegression:
    """
    Regression tests ensuring all known env vars categorize correctly.

    These tests use fixtures to verify that pattern-based inference
    produces the same results as the old hardcoded approach.
    """

    def test_all_known_vars_categorize_correctly(self, known_env_vars):
        """All known env vars get correct categories."""
        for var_name, expected in known_env_vars.items():
            actual_category = infer_category(var_name)
            assert actual_category == expected["category"], (
                f"{var_name}: expected category '{expected['category']}', "
                f"got '{actual_category}'"
            )

    def test_all_known_vars_type_correctly(self, known_env_vars):
        """All known env vars get correct type metadata."""
        for var_name, expected in known_env_vars.items():
            actual_meta = infer_type_metadata(var_name)

            if expected["type"] == "boolean":
                assert actual_meta.get("enum") == ["0", "1"], (
                    f"{var_name}: expected boolean type (enum 0/1)"
                )
            elif expected["type"] == "integer":
                assert actual_meta.get("x-value-type") == "integer", (
                    f"{var_name}: expected integer type"
                )
            else:
                # String type (default)
                assert "enum" not in actual_meta, (
                    f"{var_name}: expected string type, got boolean"
                )
                assert "x-value-type" not in actual_meta, (
                    f"{var_name}: expected string type, got integer"
                )
