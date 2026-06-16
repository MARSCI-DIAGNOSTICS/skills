#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core scripts for OpenAI Codex CLI documentation management.

This package contains the core functionality:
- llms_parser: Parse llms.txt and llms-full.txt formats
- scrape_docs: Fetch and save documentation from sources
- doc_resolver: Search and resolve documentation
- find_docs: CLI interface for documentation search
"""

from pathlib import Path

__all__ = [
    'llms_parser',
    'scrape_docs',
    'doc_resolver',
    'find_docs',
]
