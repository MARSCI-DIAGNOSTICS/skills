#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
config_helpers.py - Configuration loading utilities.

Loads configuration from defaults.yaml with environment variable overrides.
"""

import os
from pathlib import Path
from typing import Any, Optional

import yaml


def load_config(config_path: Optional[Path] = None) -> dict:
    """
    Load configuration from YAML file.

    Args:
        config_path: Path to config file. If None, uses defaults.yaml.

    Returns:
        Configuration dictionary
    """
    if config_path is None:
        # Find config relative to this file
        utils_dir = Path(__file__).parent
        scripts_dir = utils_dir.parent
        skill_dir = scripts_dir.parent
        config_path = skill_dir / 'config' / 'defaults.yaml'

    if not config_path.exists():
        return {}

    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f) or {}


def get_config_value(
    config: dict,
    section: str,
    key: str,
    default: Any = None,
    env_prefix: str = 'MILAN_BLOG'
) -> Any:
    """
    Get configuration value with environment variable override.

    Args:
        config: Configuration dictionary
        section: Config section name
        key: Config key name
        default: Default value if not found
        env_prefix: Environment variable prefix

    Returns:
        Configuration value
    """
    # Check environment variable first
    env_key = f"{env_prefix}_{section.upper()}_{key.upper()}"
    env_value = os.environ.get(env_key)
    if env_value is not None:
        # Try to parse as appropriate type
        if env_value.lower() in ('true', 'false'):
            return env_value.lower() == 'true'
        try:
            return int(env_value)
        except ValueError:
            pass
        try:
            return float(env_value)
        except ValueError:
            pass
        return env_value

    # Get from config
    section_data = config.get(section, {})
    return section_data.get(key, default)


class ConfigRegistry:
    """
    Configuration registry with lazy loading and caching.
    """

    _instance: Optional['ConfigRegistry'] = None
    _config: Optional[dict] = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    @property
    def config(self) -> dict:
        """Lazy load configuration."""
        if self._config is None:
            self._config = load_config()
        return self._config

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """Get configuration value."""
        return get_config_value(self.config, section, key, default)

    def reload(self) -> None:
        """Reload configuration from disk."""
        self._config = load_config()


# Global config instance
config = ConfigRegistry()


def get_scraping_config() -> dict:
    """Get scraping-related configuration."""
    return config.config.get('scraping', {})


def get_date_filter_config() -> dict:
    """Get date filtering configuration."""
    return config.config.get('date_filter', {})


def get_cleanup_config() -> dict:
    """Get content cleanup configuration."""
    return config.config.get('cleanup', {})


def get_search_config() -> dict:
    """Get search configuration."""
    return config.config.get('search', {})
