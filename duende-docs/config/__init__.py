"""Configuration package for duende-docs skill."""

from .config_registry import (
    ConfigRegistry,
    get_registry,
    get_default,
    load_sources,
    load_filtering,
    load_tag_detection,
    load_defaults,
    reload_configs,
)

__all__ = [
    'ConfigRegistry',
    'get_registry',
    'get_default',
    'load_sources',
    'load_filtering',
    'load_tag_detection',
    'load_defaults',
    'reload_configs',
]
