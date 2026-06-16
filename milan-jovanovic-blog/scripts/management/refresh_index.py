#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
refresh_index.py - Rebuild and refresh index with metadata extraction.

Pipeline:
1. Rebuild index from filesystem
2. Extract keywords and tags for each entry
3. Validate metadata coverage
4. Generate summary report
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

# Add parent to path for imports (bootstrap handles UTF-8)
sys.path.insert(0, str(Path(__file__).parent.parent))

from bootstrap import skill_dir
from management.index_manager import IndexManager
from management.extract_metadata import MetadataExtractor


def refresh_index(
    extract_keywords: bool = True,
    validate: bool = True,
    verbose: bool = False,
) -> dict:
    """
    Refresh the index with full metadata extraction.

    Returns statistics dict.
    """
    stats = {
        'started_at': datetime.now(timezone.utc).isoformat(),
        'rebuild': {},
        'metadata': {},
        'validation': {},
    }

    manager = IndexManager()
    # skill_dir is available from bootstrap import

    print("=" * 60)
    print("Milan Jovanovic Blog - Index Refresh")
    print("=" * 60)
    print()

    # Step 1: Rebuild from filesystem
    print("[1/3] Rebuilding index from filesystem...")
    rebuild_stats = manager.rebuild_from_filesystem()
    stats['rebuild'] = rebuild_stats

    print(f"  Files found: {rebuild_stats['files_found']}")
    print(f"  Files indexed: {rebuild_stats['files_indexed']}")
    print(f"  Errors: {rebuild_stats['errors']}")
    print()

    # Step 2: Extract metadata
    if extract_keywords:
        print("[2/3] Extracting keywords and tags...")
        extractor = MetadataExtractor()

        entries = manager.list_all()
        updated = 0
        errors = 0

        for entry in entries:
            try:
                file_path = manager.canonical_dir / entry.path
                if file_path.exists():
                    content = file_path.read_text(encoding='utf-8')

                    # Extract metadata
                    keywords = extractor.extract_keywords(content)
                    tags = extractor.detect_tags(content)
                    patterns = extractor.detect_patterns(content)

                    # Update entry
                    entry.keywords = keywords
                    entry.tags = tags
                    entry.patterns = patterns
                    manager.put(entry)
                    updated += 1

                    if verbose:
                        print(f"  {entry.doc_id}: {len(keywords)} keywords, {len(tags)} tags")
            except Exception as e:
                print(f"  Error processing {entry.doc_id}: {e}")
                errors += 1

        stats['metadata'] = {
            'entries_processed': len(entries),
            'entries_updated': updated,
            'errors': errors,
        }
        print(f"  Entries updated: {updated}")
        print(f"  Errors: {errors}")
        print()
    else:
        print("[2/3] Skipping metadata extraction")
        print()

    # Step 3: Validation
    if validate:
        print("[3/3] Validating index...")
        validation = manager.verify()
        stats['validation'] = validation

        print(f"  Total entries: {validation['total']}")
        print(f"  Valid: {validation['valid']}")

        issues = (
            len(validation['missing_files']) +
            len(validation['hash_mismatch']) +
            len(validation['missing_fields'])
        )
        if issues > 0:
            print(f"  Issues: {issues}")
        else:
            print("  ✓ All entries valid")
        print()
    else:
        print("[3/3] Skipping validation")
        print()

    stats['completed_at'] = datetime.now(timezone.utc).isoformat()

    # Summary
    print("=" * 60)
    print("Refresh Complete")
    print("=" * 60)
    print(f"Total indexed: {manager.count()}")
    print()

    return stats


def main():
    parser = argparse.ArgumentParser(
        description='Refresh Milan Jovanovic blog index',
    )
    parser.add_argument(
        '--no-keywords',
        action='store_true',
        help='Skip keyword extraction',
    )
    parser.add_argument(
        '--no-validate',
        action='store_true',
        help='Skip validation',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output stats as JSON',
    )

    args = parser.parse_args()

    stats = refresh_index(
        extract_keywords=not args.no_keywords,
        validate=not args.no_validate,
        verbose=args.verbose,
    )

    if args.json:
        print(json.dumps(stats, indent=2))


if __name__ == '__main__':
    main()
