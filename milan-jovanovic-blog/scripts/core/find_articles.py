#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
find_articles.py - Search and discovery for Milan Jovanovic blog articles.

Commands:
- search: Keyword-based search
- tag: Filter by tag
- pattern: Filter by architectural pattern
- resolve: Resolve doc_id to file path
- query: Natural language search
- list: List all articles
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bootstrap import skill_dir
from management.index_manager import IndexManager, IndexEntry


class ArticleFinder:
    """
    Article discovery and search.
    """

    def __init__(self):
        self.manager = IndexManager()
        self.skill_root = skill_dir

    def search(
        self,
        keywords: list[str],
        limit: int = 25,
        min_score: int = 0,
    ) -> list[tuple[IndexEntry, int]]:
        """
        Search articles by keywords with relevance scoring.

        Args:
            keywords: Search keywords
            limit: Maximum results
            min_score: Minimum relevance score

        Returns:
            List of (entry, score) tuples sorted by score
        """
        results = []
        keywords_lower = [k.lower() for k in keywords]

        for entry in self.manager.list_all():
            score = 0

            # Score based on field matches
            title_lower = entry.title.lower()
            desc_lower = entry.description.lower()
            entry_keywords = [k.lower() for k in entry.keywords]
            entry_tags = [t.lower() for t in entry.tags]

            for kw in keywords_lower:
                # Title match (highest weight)
                if kw in title_lower:
                    score += 10
                # Tag match
                if kw in entry_tags:
                    score += 8
                # Keyword match
                if kw in entry_keywords:
                    score += 5
                # Description match
                if kw in desc_lower:
                    score += 3

            if score >= min_score:
                results.append((entry, score))

        # Sort by score descending
        results.sort(key=lambda x: -x[1])

        return results[:limit]

    def by_tag(self, tag: str) -> list[IndexEntry]:
        """Get articles by tag."""
        return self.manager.get_by_tag(tag)

    def by_pattern(self, pattern: str) -> list[IndexEntry]:
        """Get articles by architectural pattern."""
        results = []
        pattern_lower = pattern.lower()

        for entry in self.manager.list_all():
            patterns = [p.lower() for p in entry.patterns]
            if pattern_lower in patterns:
                results.append(entry)

        return results

    def resolve(self, doc_id: str) -> Optional[Path]:
        """
        Resolve doc_id to file path.

        Args:
            doc_id: Document ID

        Returns:
            Absolute path to file or None
        """
        entry = self.manager.get(doc_id)
        if entry:
            return self.manager.canonical_dir / entry.path
        return None

    def query(self, query_text: str, limit: int = 10) -> list[tuple[IndexEntry, int]]:
        """
        Natural language query.

        Extracts keywords from query and performs search.

        Args:
            query_text: Natural language query
            limit: Maximum results

        Returns:
            List of (entry, score) tuples
        """
        # Extract meaningful words
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]+\b', query_text.lower())

        # Filter common words
        stop_words = {
            'how', 'to', 'do', 'i', 'use', 'implement', 'create', 'make',
            'what', 'is', 'the', 'best', 'way', 'for', 'in', 'with', 'a', 'an',
        }
        keywords = [w for w in words if w not in stop_words and len(w) > 2]

        return self.search(keywords, limit=limit)

    def list_all(
        self,
        sort_by: str = 'date',
        limit: Optional[int] = None,
    ) -> list[IndexEntry]:
        """
        List all articles.

        Args:
            sort_by: Sort by 'date', 'title', or 'doc_id'
            limit: Maximum results

        Returns:
            List of entries
        """
        entries = self.manager.list_all()

        if sort_by == 'date':
            entries.sort(key=lambda e: e.published_at or '', reverse=True)
        elif sort_by == 'title':
            entries.sort(key=lambda e: e.title.lower())
        elif sort_by == 'doc_id':
            entries.sort(key=lambda e: e.doc_id)

        if limit:
            entries = entries[:limit]

        return entries

    def get_tags(self) -> dict[str, int]:
        """Get all tags with counts."""
        tag_counts: dict[str, int] = {}
        for entry in self.manager.list_all():
            for tag in entry.tags:
                tag_counts[tag] = tag_counts.get(tag, 0) + 1
        return dict(sorted(tag_counts.items(), key=lambda x: -x[1]))

    def get_patterns(self) -> dict[str, int]:
        """Get all patterns with counts."""
        pattern_counts: dict[str, int] = {}
        for entry in self.manager.list_all():
            for pattern in entry.patterns:
                pattern_counts[pattern] = pattern_counts.get(pattern, 0) + 1
        return dict(sorted(pattern_counts.items(), key=lambda x: -x[1]))


def cmd_search(args, finder: ArticleFinder):
    """Search command."""
    results = finder.search(
        args.keywords,
        limit=args.limit,
        min_score=args.min_score,
    )

    if args.json:
        data = [{'entry': e.to_dict(), 'score': s} for e, s in results]
        print(json.dumps(data, indent=2))
    else:
        if not results:
            print("No results found.")
            return

        total = len(finder.manager.list_all())
        print(f"Found {len(results)} results (showing {len(results)} of {total}):\n")

        for entry, score in results:
            if args.verbose:
                print(f"[score: {score}] {entry.doc_id}")
                print(f"  Title: {entry.title}")
                print(f"  Tags: {', '.join(entry.tags) if entry.tags else 'none'}")
                print()
            else:
                print(f"  {entry.doc_id}: {entry.title}")


def cmd_tag(args, finder: ArticleFinder):
    """Tag filter command."""
    if args.list:
        tags = finder.get_tags()
        if args.json:
            print(json.dumps(tags, indent=2))
        else:
            print("Tags:")
            for tag, count in tags.items():
                print(f"  {tag}: {count}")
        return

    results = finder.by_tag(args.tag)

    if args.json:
        print(json.dumps([e.to_dict() for e in results], indent=2))
    else:
        print(f"Articles with tag '{args.tag}' ({len(results)}):\n")
        for entry in results:
            print(f"  {entry.doc_id}: {entry.title}")


def cmd_pattern(args, finder: ArticleFinder):
    """Pattern filter command."""
    if args.list:
        patterns = finder.get_patterns()
        if args.json:
            print(json.dumps(patterns, indent=2))
        else:
            print("Patterns:")
            for pattern, count in patterns.items():
                print(f"  {pattern}: {count}")
        return

    results = finder.by_pattern(args.pattern)

    if args.json:
        print(json.dumps([e.to_dict() for e in results], indent=2))
    else:
        print(f"Articles with pattern '{args.pattern}' ({len(results)}):\n")
        for entry in results:
            print(f"  {entry.doc_id}: {entry.title}")


def cmd_resolve(args, finder: ArticleFinder):
    """Resolve doc_id command."""
    path = finder.resolve(args.doc_id)

    if path:
        if args.json:
            print(json.dumps({'doc_id': args.doc_id, 'path': str(path)}))
        else:
            print(path)
    else:
        print(f"Not found: {args.doc_id}", file=sys.stderr)
        sys.exit(1)


def cmd_query(args, finder: ArticleFinder):
    """Natural language query command."""
    results = finder.query(args.query, limit=args.limit)

    if args.json:
        data = [{'entry': e.to_dict(), 'score': s} for e, s in results]
        print(json.dumps(data, indent=2))
    else:
        if not results:
            print("No results found.")
            return

        print(f"Results for: \"{args.query}\"\n")
        for entry, score in results:
            print(f"  [{score}] {entry.title}")
            print(f"      {entry.doc_id}")
            print()


def cmd_list(args, finder: ArticleFinder):
    """List all articles command."""
    entries = finder.list_all(sort_by=args.sort, limit=args.limit)

    if args.json:
        print(json.dumps([e.to_dict() for e in entries], indent=2))
    else:
        total = len(finder.manager.list_all())
        shown = len(entries)
        print(f"Articles ({shown} of {total}):\n")

        for entry in entries:
            date = entry.published_at[:10] if entry.published_at else 'unknown'
            print(f"  [{date}] {entry.title}")
            if args.verbose:
                print(f"           {entry.doc_id}")


def main():
    parser = argparse.ArgumentParser(
        description='Find Milan Jovanovic blog articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Search by keywords
  python find_articles.py search clean architecture cqrs

  # Filter by tag
  python find_articles.py tag ef-core

  # List all tags
  python find_articles.py tag --list

  # Resolve doc_id
  python find_articles.py resolve milanjovanovic-tech-blog-some-slug

  # Natural language query
  python find_articles.py query "how to implement CQRS"

  # List recent articles
  python find_articles.py list --sort date --limit 10
        """,
    )

    # Global options
    parser.add_argument('--json', action='store_true', help='JSON output')
    parser.add_argument('--limit', type=int, default=25, help='Max results')
    parser.add_argument('-v', '--verbose', action='store_true')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # search
    search_p = subparsers.add_parser('search', help='Keyword search')
    search_p.add_argument('keywords', nargs='+', help='Search keywords')
    search_p.add_argument('--min-score', type=int, default=0)

    # tag
    tag_p = subparsers.add_parser('tag', help='Filter by tag')
    tag_p.add_argument('tag', nargs='?', help='Tag name')
    tag_p.add_argument('--list', action='store_true', help='List all tags')

    # pattern
    pattern_p = subparsers.add_parser('pattern', help='Filter by pattern')
    pattern_p.add_argument('pattern', nargs='?', help='Pattern name')
    pattern_p.add_argument('--list', action='store_true', help='List all patterns')

    # resolve
    resolve_p = subparsers.add_parser('resolve', help='Resolve doc_id')
    resolve_p.add_argument('doc_id', help='Document ID')

    # query
    query_p = subparsers.add_parser('query', help='Natural language query')
    query_p.add_argument('query', help='Query text')

    # list
    list_p = subparsers.add_parser('list', help='List all articles')
    list_p.add_argument('--sort', choices=['date', 'title', 'doc_id'], default='date')

    args = parser.parse_args()

    finder = ArticleFinder()

    commands = {
        'search': cmd_search,
        'tag': cmd_tag,
        'pattern': cmd_pattern,
        'resolve': cmd_resolve,
        'query': cmd_query,
        'list': cmd_list,
    }

    commands[args.command](args, finder)


if __name__ == '__main__':
    main()
