#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
manage_index.py - CLI wrapper for index management operations.

Provides unified CLI for:
- Index CRUD operations
- Verification and validation
- Statistics and reporting
"""

import argparse
import json
import sys
from pathlib import Path

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from management.index_manager import IndexManager


def cmd_count(args, manager: IndexManager):
    """Show entry count."""
    count = manager.count()
    if args.json:
        print(json.dumps({'count': count}))
    else:
        print(f"Total entries: {count}")


def cmd_list(args, manager: IndexManager):
    """List all entries."""
    entries = manager.list_all()

    if args.json:
        print(json.dumps([e.to_dict() for e in entries], indent=2))
    else:
        if not entries:
            print("No entries in index.")
            return

        for entry in entries:
            if args.verbose:
                date = entry.published_at[:10] if entry.published_at else 'unknown'
                print(f"[{date}] {entry.doc_id}")
                print(f"  Title: {entry.title}")
                print(f"  URL: {entry.source_url}")
                print()
            else:
                print(f"{entry.doc_id}: {entry.title}")


def cmd_get(args, manager: IndexManager):
    """Get entry by doc_id."""
    entry = manager.get(args.doc_id)
    if entry:
        if args.json:
            print(json.dumps(entry.to_dict(), indent=2))
        else:
            print(f"doc_id: {entry.doc_id}")
            print(f"title: {entry.title}")
            print(f"source_url: {entry.source_url}")
            print(f"published_at: {entry.published_at}")
            print(f"path: {entry.path}")
            if entry.tags:
                print(f"tags: {', '.join(entry.tags)}")
            if entry.keywords:
                print(f"keywords: {', '.join(entry.keywords[:10])}")
    else:
        print(f"Not found: {args.doc_id}", file=sys.stderr)
        sys.exit(1)


def cmd_search(args, manager: IndexManager):
    """Search entries."""
    results = manager.search(args.query)

    if args.json:
        print(json.dumps([e.to_dict() for e in results], indent=2))
    else:
        if not results:
            print(f"No results for: {args.query}")
            return

        print(f"Found {len(results)} results:")
        for entry in results:
            print(f"  {entry.doc_id}: {entry.title}")


def cmd_verify(args, manager: IndexManager):
    """Verify index integrity."""
    results = manager.verify()

    if args.json:
        print(json.dumps(results, indent=2))
    else:
        print(f"Total entries: {results['total']}")
        print(f"Valid: {results['valid']}")

        if results['missing_files']:
            print(f"\nMissing files ({len(results['missing_files'])}):")
            for doc_id in results['missing_files'][:5]:
                print(f"  - {doc_id}")
            if len(results['missing_files']) > 5:
                print(f"  ... and {len(results['missing_files']) - 5} more")

        if results['hash_mismatch']:
            print(f"\nHash mismatches ({len(results['hash_mismatch'])}):")
            for doc_id in results['hash_mismatch'][:5]:
                print(f"  - {doc_id}")

        if results['missing_fields']:
            print(f"\nMissing required fields ({len(results['missing_fields'])}):")
            for doc_id in results['missing_fields'][:5]:
                print(f"  - {doc_id}")

        # Summary
        issues = (
            len(results['missing_files']) +
            len(results['hash_mismatch']) +
            len(results['missing_fields'])
        )
        if issues == 0:
            print("\n✓ All entries valid")
        else:
            print(f"\n⚠ {issues} issues found")
            sys.exit(1)


def cmd_rebuild(args, manager: IndexManager):
    """Rebuild index from filesystem."""
    if not args.yes:
        print("This will rebuild the index from filesystem.")
        print("Existing index will be overwritten.")
        response = input("Continue? [y/N] ")
        if response.lower() != 'y':
            print("Aborted.")
            return

    stats = manager.rebuild_from_filesystem()

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(f"Files found: {stats['files_found']}")
        print(f"Files indexed: {stats['files_indexed']}")
        print(f"Errors: {stats['errors']}")


def cmd_stats(args, manager: IndexManager):
    """Show index statistics."""
    stats = manager.get_stats()

    if args.json:
        print(json.dumps(stats, indent=2))
    else:
        print(f"Total entries: {stats['total_entries']}")
        print(f"Index path: {stats['index_path']}")

        if stats['by_month']:
            print("\nBy month:")
            for month, count in list(stats['by_month'].items())[:12]:
                print(f"  {month}: {count}")

        if stats['by_tag']:
            print("\nTop tags:")
            for tag, count in list(stats['by_tag'].items())[:10]:
                print(f"  {tag}: {count}")


def main():
    parser = argparse.ArgumentParser(
        description='Manage Milan Jovanovic blog article index',
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    # Global options
    parser.add_argument('--json', action='store_true', help='JSON output')

    subparsers = parser.add_subparsers(dest='command', required=True)

    # count
    subparsers.add_parser('count', help='Show entry count')

    # list
    list_p = subparsers.add_parser('list', help='List all entries')
    list_p.add_argument('-v', '--verbose', action='store_true')

    # get
    get_p = subparsers.add_parser('get', help='Get entry by doc_id')
    get_p.add_argument('doc_id', help='Document ID')

    # search
    search_p = subparsers.add_parser('search', help='Search entries')
    search_p.add_argument('query', help='Search query')

    # verify
    subparsers.add_parser('verify', help='Verify index integrity')

    # rebuild
    rebuild_p = subparsers.add_parser('rebuild', help='Rebuild from filesystem')
    rebuild_p.add_argument('-y', '--yes', action='store_true', help='Skip confirmation')

    # stats
    subparsers.add_parser('stats', help='Show statistics')

    args = parser.parse_args()

    manager = IndexManager()

    commands = {
        'count': cmd_count,
        'list': cmd_list,
        'get': cmd_get,
        'search': cmd_search,
        'verify': cmd_verify,
        'rebuild': cmd_rebuild,
        'stats': cmd_stats,
    }

    commands[args.command](args, manager)


if __name__ == '__main__':
    main()
