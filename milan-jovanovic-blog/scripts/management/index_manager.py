#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
index_manager.py - Index management for Milan Jovanovic blog articles.

Provides:
- Index CRUD operations
- Content hash verification
- Index rebuilding from filesystem
- Statistics and reporting
"""

import hashlib
import json
import re
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bootstrap import skill_dir


@dataclass
class IndexEntry:
    """Single index entry for an article."""
    doc_id: str
    title: str
    description: str
    path: str
    source_url: str
    published_at: Optional[str] = None
    last_fetched: Optional[str] = None
    content_hash: Optional[str] = None
    keywords: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    patterns: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        """Convert to dictionary."""
        return {
            'doc_id': self.doc_id,
            'title': self.title,
            'description': self.description,
            'path': self.path,
            'source_url': self.source_url,
            'published_at': self.published_at,
            'last_fetched': self.last_fetched,
            'content_hash': self.content_hash,
            'keywords': self.keywords,
            'tags': self.tags,
            'patterns': self.patterns,
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'IndexEntry':
        """Create from dictionary."""
        return cls(
            doc_id=data['doc_id'],
            title=data['title'],
            description=data.get('description', ''),
            path=data['path'],
            source_url=data['source_url'],
            published_at=data.get('published_at'),
            last_fetched=data.get('last_fetched'),
            content_hash=data.get('content_hash'),
            keywords=data.get('keywords', []),
            tags=data.get('tags', []),
            patterns=data.get('patterns', []),
        )


class IndexManager:
    """
    Manages the article index.

    The index is a JSON file mapping doc_id to article metadata.
    """

    def __init__(self, index_path: Optional[Path] = None):
        self.skill_root = skill_dir
        self.canonical_dir = self.skill_root / 'canonical'
        self.index_path = index_path or (self.canonical_dir / 'index.json')
        self._index: Optional[dict] = None

    @property
    def index(self) -> dict:
        """Lazy load index."""
        if self._index is None:
            self._index = self._load()
        return self._index

    def _load(self) -> dict:
        """Load index from disk."""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save(self) -> None:
        """Save index to disk."""
        self.index_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def get(self, doc_id: str) -> Optional[IndexEntry]:
        """Get entry by doc_id."""
        data = self.index.get(doc_id)
        if data:
            return IndexEntry.from_dict(data)
        return None

    def put(self, entry: IndexEntry) -> None:
        """Add or update entry."""
        self.index[entry.doc_id] = entry.to_dict()
        self._save()

    def delete(self, doc_id: str) -> bool:
        """Delete entry by doc_id."""
        if doc_id in self.index:
            del self.index[doc_id]
            self._save()
            return True
        return False

    def list_all(self) -> list[IndexEntry]:
        """List all entries."""
        return [IndexEntry.from_dict(data) for data in self.index.values()]

    def count(self) -> int:
        """Get total entry count."""
        return len(self.index)

    def search(self, query: str) -> list[IndexEntry]:
        """
        Search entries by query.

        Searches title, description, keywords, tags.
        """
        query_lower = query.lower()
        results = []

        for data in self.index.values():
            # Search in multiple fields
            searchable = ' '.join([
                data.get('title', ''),
                data.get('description', ''),
                ' '.join(data.get('keywords', [])),
                ' '.join(data.get('tags', [])),
            ]).lower()

            if query_lower in searchable:
                results.append(IndexEntry.from_dict(data))

        return results

    def get_by_tag(self, tag: str) -> list[IndexEntry]:
        """Get entries by tag."""
        results = []
        tag_lower = tag.lower()

        for data in self.index.values():
            tags = [t.lower() for t in data.get('tags', [])]
            if tag_lower in tags:
                results.append(IndexEntry.from_dict(data))

        return results

    def verify(self) -> dict:
        """
        Verify index integrity.

        Checks:
        - All indexed files exist
        - Content hashes match
        - Required fields present

        Returns dict with verification results.
        """
        results = {
            'total': self.count(),
            'valid': 0,
            'missing_files': [],
            'hash_mismatch': [],
            'missing_fields': [],
        }

        for doc_id, data in self.index.items():
            entry = IndexEntry.from_dict(data)

            # Check file exists
            file_path = self.canonical_dir / entry.path
            if not file_path.exists():
                results['missing_files'].append(doc_id)
                continue

            # Check required fields
            if not entry.title or not entry.source_url:
                results['missing_fields'].append(doc_id)
                continue

            # Verify content hash if present
            if entry.content_hash:
                content = file_path.read_text(encoding='utf-8')
                # Extract content after frontmatter
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        content = parts[2].strip()

                computed_hash = f"sha256:{hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]}"
                if computed_hash != entry.content_hash:
                    results['hash_mismatch'].append(doc_id)
                    continue

            results['valid'] += 1

        return results

    def rebuild_from_filesystem(self) -> dict:
        """
        Rebuild index from filesystem.

        Scans canonical directory for .md files and extracts metadata.
        Returns statistics dict.
        """
        stats = {
            'files_found': 0,
            'files_indexed': 0,
            'errors': 0,
        }

        # Clear existing index
        self._index = {}

        # Find all markdown files
        blog_dir = self.canonical_dir / 'milanjovanovic-tech' / 'blog'
        if not blog_dir.exists():
            return stats

        for md_file in blog_dir.glob('*.md'):
            stats['files_found'] += 1

            try:
                content = md_file.read_text(encoding='utf-8')
                entry = self._parse_file(md_file, content)
                if entry:
                    self.index[entry.doc_id] = entry.to_dict()
                    stats['files_indexed'] += 1
            except Exception as e:
                print(f"Error parsing {md_file}: {e}")
                stats['errors'] += 1

        self._save()
        return stats

    def _parse_file(self, file_path: Path, content: str) -> Optional[IndexEntry]:
        """Parse markdown file to extract index entry."""
        # Extract frontmatter
        if not content.startswith('---'):
            return None

        parts = content.split('---', 2)
        if len(parts) < 3:
            return None

        frontmatter = parts[1]
        body = parts[2].strip()

        # Parse frontmatter fields
        metadata = {}
        for line in frontmatter.strip().split('\n'):
            if ':' in line:
                key, value = line.split(':', 1)
                metadata[key.strip()] = value.strip().strip('"')

        # Generate content hash
        content_hash = f"sha256:{hashlib.sha256(body.encode('utf-8')).hexdigest()[:16]}"

        # Extract description from body
        desc_match = re.search(r'^#[^\n]+\n+([^\n#]+)', body)
        description = desc_match.group(1).strip()[:200] if desc_match else ''

        return IndexEntry(
            doc_id=metadata.get('doc_id', file_path.stem),
            title=metadata.get('title', file_path.stem),
            description=description,
            path=str(file_path.relative_to(self.canonical_dir)),
            source_url=metadata.get('source_url', ''),
            published_at=metadata.get('published_at') or metadata.get('date'),
            last_fetched=metadata.get('last_fetched'),
            content_hash=content_hash,
        )

    def get_stats(self) -> dict:
        """Get index statistics."""
        entries = self.list_all()

        # Count by month
        by_month: dict[str, int] = {}
        for entry in entries:
            if entry.published_at:
                month = entry.published_at[:7]  # YYYY-MM
                by_month[month] = by_month.get(month, 0) + 1

        # Count by tag
        by_tag: dict[str, int] = {}
        for entry in entries:
            for tag in entry.tags:
                by_tag[tag] = by_tag.get(tag, 0) + 1

        return {
            'total_entries': len(entries),
            'by_month': dict(sorted(by_month.items(), reverse=True)),
            'by_tag': dict(sorted(by_tag.items(), key=lambda x: -x[1])),
            'index_path': str(self.index_path),
        }


def main():
    """CLI for index management."""
    import argparse

    parser = argparse.ArgumentParser(
        description='Manage Milan Jovanovic blog article index',
    )
    subparsers = parser.add_subparsers(dest='command', required=True)

    # Count command
    subparsers.add_parser('count', help='Show entry count')

    # List command
    list_parser = subparsers.add_parser('list', help='List all entries')
    list_parser.add_argument('--json', action='store_true', help='JSON output')

    # Get command
    get_parser = subparsers.add_parser('get', help='Get entry by doc_id')
    get_parser.add_argument('doc_id', help='Document ID')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search entries')
    search_parser.add_argument('query', help='Search query')

    # Verify command
    subparsers.add_parser('verify', help='Verify index integrity')

    # Rebuild command
    subparsers.add_parser('rebuild', help='Rebuild index from filesystem')

    # Stats command
    subparsers.add_parser('stats', help='Show index statistics')

    args = parser.parse_args()

    manager = IndexManager()

    if args.command == 'count':
        print(f"Total entries: {manager.count()}")

    elif args.command == 'list':
        entries = manager.list_all()
        if hasattr(args, 'json') and args.json:
            print(json.dumps([e.to_dict() for e in entries], indent=2))
        else:
            for entry in entries:
                print(f"{entry.doc_id}: {entry.title}")

    elif args.command == 'get':
        entry = manager.get(args.doc_id)
        if entry:
            print(json.dumps(entry.to_dict(), indent=2))
        else:
            print(f"Not found: {args.doc_id}")
            sys.exit(1)

    elif args.command == 'search':
        results = manager.search(args.query)
        print(f"Found {len(results)} results:")
        for entry in results:
            print(f"  {entry.doc_id}: {entry.title}")

    elif args.command == 'verify':
        results = manager.verify()
        print(f"Total: {results['total']}")
        print(f"Valid: {results['valid']}")
        if results['missing_files']:
            print(f"Missing files: {len(results['missing_files'])}")
        if results['hash_mismatch']:
            print(f"Hash mismatches: {len(results['hash_mismatch'])}")
        if results['missing_fields']:
            print(f"Missing fields: {len(results['missing_fields'])}")

    elif args.command == 'rebuild':
        stats = manager.rebuild_from_filesystem()
        print(f"Files found: {stats['files_found']}")
        print(f"Files indexed: {stats['files_indexed']}")
        print(f"Errors: {stats['errors']}")

    elif args.command == 'stats':
        stats = manager.get_stats()
        print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
