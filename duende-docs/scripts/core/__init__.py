#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Core scripts for Duende documentation management.

This package contains the core functionality:
- llms_full_parser: Parse Duende's llms-full.txt format (pre-rendered markdown)
- scrape_docs: Fetch and save documentation from sources
- doc_resolver: Search and resolve documentation
- find_docs: CLI interface for documentation search
"""

from pathlib import Path

__all__ = [
    'llms_full_parser',
    'scrape_docs',
    'doc_resolver',
    'find_docs',
]
