#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
milan_jovanovic_api.py - Public Python API for Milan Jovanovic blog skill.

Provides clean interface for:
- Article search and discovery
- Tag and pattern filtering
- Doc ID resolution
- Content retrieval
"""

import sys
from pathlib import Path
from typing import Optional

# Add scripts to path for imports
_skill_root = Path(__file__).parent
sys.path.insert(0, str(_skill_root / 'scripts'))

from core.find_articles import ArticleFinder
from core.article_resolver import ArticleResolver
from management.index_manager import IndexManager, IndexEntry


# Lazy-loaded singletons
_finder: Optional[ArticleFinder] = None
_resolver: Optional[ArticleResolver] = None
_manager: Optional[IndexManager] = None


def _get_finder() -> ArticleFinder:
    """Get or create ArticleFinder singleton."""
    global _finder
    if _finder is None:
        _finder = ArticleFinder()
    return _finder


def _get_resolver() -> ArticleResolver:
    """Get or create ArticleResolver singleton."""
    global _resolver
    if _resolver is None:
        _resolver = ArticleResolver()
    return _resolver


def _get_manager() -> IndexManager:
    """Get or create IndexManager singleton."""
    global _manager
    if _manager is None:
        _manager = IndexManager()
    return _manager


# ============================================================================
# Search and Discovery
# ============================================================================

def search_articles(
    keywords: list[str],
    limit: int = 25,
    min_score: int = 0,
) -> list[dict]:
    """
    Search articles by keywords.

    Args:
        keywords: Search keywords
        limit: Maximum results (default 25)
        min_score: Minimum relevance score (default 0)

    Returns:
        List of dicts with 'entry' and 'score' keys
    """
    finder = _get_finder()
    results = finder.search(keywords, limit=limit, min_score=min_score)
    return [{'entry': e.to_dict(), 'score': s} for e, s in results]


def query_articles(query: str, limit: int = 10) -> list[dict]:
    """
    Natural language query.

    Args:
        query: Natural language query text
        limit: Maximum results

    Returns:
        List of dicts with 'entry' and 'score' keys
    """
    finder = _get_finder()
    results = finder.query(query, limit=limit)
    return [{'entry': e.to_dict(), 'score': s} for e, s in results]


def list_articles(
    sort_by: str = 'date',
    limit: Optional[int] = None,
) -> list[dict]:
    """
    List all articles.

    Args:
        sort_by: Sort by 'date', 'title', or 'doc_id'
        limit: Maximum results

    Returns:
        List of article dicts
    """
    finder = _get_finder()
    entries = finder.list_all(sort_by=sort_by, limit=limit)
    return [e.to_dict() for e in entries]


# ============================================================================
# Tag and Pattern Filtering
# ============================================================================

def get_by_tag(tag: str) -> list[dict]:
    """
    Get articles by tag.

    Args:
        tag: Tag name (e.g., 'clean-architecture', 'ddd', 'ef-core')

    Returns:
        List of article dicts
    """
    finder = _get_finder()
    entries = finder.by_tag(tag)
    return [e.to_dict() for e in entries]


def get_by_pattern(pattern: str) -> list[dict]:
    """
    Get articles by architectural pattern.

    Args:
        pattern: Pattern name (e.g., 'minimal-apis', 'dependency-injection')

    Returns:
        List of article dicts
    """
    finder = _get_finder()
    entries = finder.by_pattern(pattern)
    return [e.to_dict() for e in entries]


def get_all_tags() -> dict[str, int]:
    """
    Get all tags with article counts.

    Returns:
        Dict mapping tag names to counts
    """
    finder = _get_finder()
    return finder.get_tags()


def get_all_patterns() -> dict[str, int]:
    """
    Get all patterns with article counts.

    Returns:
        Dict mapping pattern names to counts
    """
    finder = _get_finder()
    return finder.get_patterns()


# ============================================================================
# Resolution and Content
# ============================================================================

def resolve_doc_id(doc_id: str) -> Optional[str]:
    """
    Resolve doc_id to file path.

    Args:
        doc_id: Document ID

    Returns:
        Absolute file path as string, or None if not found
    """
    resolver = _get_resolver()
    path = resolver.resolve(doc_id)
    return str(path) if path else None


def resolve_fuzzy(partial: str, threshold: float = 0.6) -> list[dict]:
    """
    Fuzzy match doc_id.

    Args:
        partial: Partial doc_id or slug
        threshold: Minimum similarity (0-1)

    Returns:
        List of dicts with 'doc_id', 'title', 'similarity' keys
    """
    resolver = _get_resolver()
    results = resolver.resolve_fuzzy(partial, threshold)
    return [
        {'doc_id': e.doc_id, 'title': e.title, 'similarity': s}
        for e, s in results
    ]


def get_article_content(doc_id: str) -> Optional[str]:
    """
    Get article content by doc_id.

    Args:
        doc_id: Document ID

    Returns:
        Article content (markdown, without frontmatter), or None
    """
    resolver = _get_resolver()
    return resolver.get_content(doc_id)


def get_article_metadata(doc_id: str) -> Optional[dict]:
    """
    Get article metadata by doc_id.

    Args:
        doc_id: Document ID

    Returns:
        Article metadata dict, or None
    """
    resolver = _get_resolver()
    return resolver.get_metadata(doc_id)


# ============================================================================
# Index Management
# ============================================================================

def get_index_stats() -> dict:
    """
    Get index statistics.

    Returns:
        Dict with total_entries, by_month, by_tag
    """
    manager = _get_manager()
    return manager.get_stats()


def get_article_count() -> int:
    """
    Get total article count.

    Returns:
        Number of indexed articles
    """
    manager = _get_manager()
    return manager.count()


def verify_index() -> dict:
    """
    Verify index integrity.

    Returns:
        Dict with total, valid, missing_files, hash_mismatch, missing_fields
    """
    manager = _get_manager()
    return manager.verify()


# ============================================================================
# Convenience Functions
# ============================================================================

def find_relevant_articles(
    project_patterns: list[str],
    limit: int = 10,
) -> list[dict]:
    """
    Find articles relevant to a project based on detected patterns.

    This is a convenience function for the blog-advisor agent.

    Args:
        project_patterns: List of patterns detected in project
            (e.g., ['mediatr', 'ef-core', 'clean-architecture'])
        limit: Maximum articles per pattern

    Returns:
        List of relevant articles with match info
    """
    finder = _get_finder()
    results = []
    seen_ids = set()

    for pattern in project_patterns:
        # Try as tag first
        entries = finder.by_tag(pattern)

        # Try as pattern if no tag matches
        if not entries:
            entries = finder.by_pattern(pattern)

        # Add unseen entries
        for entry in entries[:limit]:
            if entry.doc_id not in seen_ids:
                seen_ids.add(entry.doc_id)
                results.append({
                    'entry': entry.to_dict(),
                    'matched_pattern': pattern,
                })

    return results
