#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
article_resolver.py - Doc ID resolution for Milan Jovanovic blog articles.

Provides simple doc_id to file path resolution with fuzzy matching.
"""

import argparse
import json
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bootstrap import skill_dir
from management.index_manager import IndexManager, IndexEntry


class ArticleResolver:
    """
    Resolves doc_id references to file paths.

    Supports:
    - Exact doc_id match
    - Partial/fuzzy doc_id match
    - URL-based resolution
    """

    def __init__(self):
        self.manager = IndexManager()
        self.skill_root = skill_dir

    def resolve(self, doc_id: str) -> Optional[Path]:
        """
        Resolve exact doc_id to file path.

        Args:
            doc_id: Document ID

        Returns:
            Absolute path or None
        """
        entry = self.manager.get(doc_id)
        if entry:
            return self.manager.canonical_dir / entry.path
        return None

    def resolve_fuzzy(
        self,
        partial: str,
        threshold: float = 0.6,
    ) -> list[tuple[IndexEntry, float]]:
        """
        Fuzzy match doc_id.

        Args:
            partial: Partial doc_id or slug
            threshold: Minimum similarity (0-1)

        Returns:
            List of (entry, similarity) tuples
        """
        results = []
        partial_lower = partial.lower()

        for entry in self.manager.list_all():
            # Check similarity against doc_id
            similarity = SequenceMatcher(
                None,
                partial_lower,
                entry.doc_id.lower(),
            ).ratio()

            if similarity >= threshold:
                results.append((entry, similarity))
                continue

            # Check against slug portion only
            slug = entry.doc_id.replace('milanjovanovic-tech-blog-', '')
            slug_similarity = SequenceMatcher(
                None,
                partial_lower,
                slug.lower(),
            ).ratio()

            if slug_similarity >= threshold:
                results.append((entry, slug_similarity))
                continue

            # Check if partial is contained in doc_id
            if partial_lower in entry.doc_id.lower():
                results.append((entry, 0.8))

        # Sort by similarity descending
        results.sort(key=lambda x: -x[1])
        return results

    def resolve_by_url(self, url: str) -> Optional[IndexEntry]:
        """
        Resolve by source URL.

        Args:
            url: Article URL

        Returns:
            Index entry or None
        """
        url_lower = url.lower().rstrip('/')

        for entry in self.manager.list_all():
            if entry.source_url.lower().rstrip('/') == url_lower:
                return entry

        return None

    def get_content(self, doc_id: str) -> Optional[str]:
        """
        Get article content by doc_id.

        Args:
            doc_id: Document ID

        Returns:
            Article content (without frontmatter) or None
        """
        path = self.resolve(doc_id)
        if not path or not path.exists():
            return None

        content = path.read_text(encoding='utf-8')

        # Strip frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()

        return content

    def get_metadata(self, doc_id: str) -> Optional[dict]:
        """
        Get article metadata by doc_id.

        Args:
            doc_id: Document ID

        Returns:
            Metadata dict or None
        """
        entry = self.manager.get(doc_id)
        if entry:
            return entry.to_dict()
        return None


def main():
    parser = argparse.ArgumentParser(
        description='Resolve Milan Jovanovic article references',
    )

    parser.add_argument('--json', action='store_true', help='JSON output')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # exact
    exact_p = subparsers.add_parser('exact', help='Exact doc_id resolution')
    exact_p.add_argument('doc_id', help='Document ID')

    # fuzzy
    fuzzy_p = subparsers.add_parser('fuzzy', help='Fuzzy doc_id match')
    fuzzy_p.add_argument('partial', help='Partial doc_id or slug')
    fuzzy_p.add_argument('--threshold', type=float, default=0.6)

    # url
    url_p = subparsers.add_parser('url', help='Resolve by URL')
    url_p.add_argument('url', help='Article URL')

    # content
    content_p = subparsers.add_parser('content', help='Get article content')
    content_p.add_argument('doc_id', help='Document ID')

    # metadata
    meta_p = subparsers.add_parser('metadata', help='Get article metadata')
    meta_p.add_argument('doc_id', help='Document ID')

    args = parser.parse_args()

    resolver = ArticleResolver()

    if args.command == 'exact':
        path = resolver.resolve(args.doc_id)
        if path:
            if args.json:
                print(json.dumps({'path': str(path)}))
            else:
                print(path)
        else:
            print(f"Not found: {args.doc_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'fuzzy':
        results = resolver.resolve_fuzzy(args.partial, args.threshold)
        if args.json:
            data = [
                {'doc_id': e.doc_id, 'title': e.title, 'similarity': s}
                for e, s in results
            ]
            print(json.dumps(data, indent=2))
        else:
            if not results:
                print(f"No matches for: {args.partial}")
                sys.exit(1)
            print(f"Matches for '{args.partial}':")
            for entry, sim in results[:10]:
                print(f"  [{sim:.2f}] {entry.doc_id}")
                print(f"         {entry.title}")

    elif args.command == 'url':
        entry = resolver.resolve_by_url(args.url)
        if entry:
            if args.json:
                print(json.dumps(entry.to_dict(), indent=2))
            else:
                print(f"doc_id: {entry.doc_id}")
                print(f"title: {entry.title}")
                print(f"path: {entry.path}")
        else:
            print(f"Not found: {args.url}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'content':
        content = resolver.get_content(args.doc_id)
        if content:
            print(content)
        else:
            print(f"Not found: {args.doc_id}", file=sys.stderr)
            sys.exit(1)

    elif args.command == 'metadata':
        metadata = resolver.get_metadata(args.doc_id)
        if metadata:
            print(json.dumps(metadata, indent=2))
        else:
            print(f"Not found: {args.doc_id}", file=sys.stderr)
            sys.exit(1)


if __name__ == '__main__':
    main()
