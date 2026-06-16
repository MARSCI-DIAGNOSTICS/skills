#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
bootstrap.py - Minimal bootstrap module for milan-jovanovic-blog scripts.

This module provides a single entry point for path setup.

Usage:
    from bootstrap import setup
    skill_dir, scripts_dir, config_dir = setup()

    # Or for simple import:
    import bootstrap
    # skill_dir, scripts_dir, config_dir are available as attributes
"""

import io
import sys
from pathlib import Path

# Force UTF-8 output on Windows to handle Unicode characters
if sys.platform == 'win32':
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')


def _find_scripts_dir(from_path: Path | None = None) -> Path:
    """Find the scripts directory by walking up from caller location."""
    if from_path is None:
        return Path(__file__).resolve().parent

    from_path = Path(from_path).resolve()
    current = from_path if from_path.is_dir() else from_path.parent
    while current != current.parent:
        if current.name == 'scripts' and (current / 'bootstrap.py').exists():
            return current
        current = current.parent

    return Path(__file__).resolve().parent


def setup(from_path: Path | None = None) -> tuple[Path, Path, Path]:
    """Setup sys.path and return key directories.

    Returns:
        Tuple of (skill_dir, scripts_dir, config_dir) as absolute paths
    """
    scripts_dir = _find_scripts_dir(from_path)
    skill_dir = scripts_dir.parent
    config_dir = skill_dir / 'config'

    for path_dir in [scripts_dir, config_dir]:
        path_str = str(path_dir)
        if path_str not in sys.path:
            sys.path.insert(0, path_str)

    return skill_dir, scripts_dir, config_dir


# Auto-setup when imported
_skill_dir, _scripts_dir, _config_dir = setup()

# Apply dev mode override if MILAN_BLOG_DEV_ROOT is set
import os
_dev_root = os.environ.get('MILAN_BLOG_DEV_ROOT')
if _dev_root:
    _dev_path = Path(_dev_root)
    if _dev_path.exists() and (_dev_path / 'SKILL.md').exists():
        _skill_dir = _dev_path
        _scripts_dir = _skill_dir / 'scripts'
        _config_dir = _skill_dir / 'config'
        for path_dir in [_scripts_dir, _config_dir]:
            path_str = str(path_dir)
            if path_str not in sys.path:
                sys.path.insert(0, path_str)
        print(f"[DEV MODE] Using: {_skill_dir}", file=sys.stderr)

# Export for scripts
skill_dir = _skill_dir
scripts_dir = _scripts_dir
config_dir = _config_dir
