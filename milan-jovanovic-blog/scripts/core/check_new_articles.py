#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_new_articles.py - Quick pre-check for new articles.

Efficiently determines which articles need scraping by:
1. Loading existing index (already scraped articles)
2. Parsing blog listing page for dates (no per-article scraping)
3. Returning only NEW articles within date range

This avoids scraping individual articles just to check dates.
"""

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional
from urllib.parse import urlparse

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bootstrap import skill_dir
from management.index_manager import IndexManager
from utils.date_filter import (
    get_cutoff_date,
    get_rolling_cutoff,
    parse_date,
    ROLLING_WINDOW_MONTHS,
)


@dataclass
class ArticleInfo:
    """Article info extracted from listing page."""
    url: str
    slug: str
    title: str
    date: Optional[datetime]
    in_index: bool = False
    within_date_range: bool = False
    content_hash: Optional[str] = None  # From index, for force mode comparison


def extract_slug(url: str) -> str:
    """Extract article slug from URL."""
    path = urlparse(url).path
    # /blog/article-slug -> article-slug
    parts = path.strip('/').split('/')
    return parts[-1] if parts else ''


def slug_to_doc_id(slug: str) -> str:
    """Convert slug to doc_id format."""
    return f"milanjovanovic-tech-blog-{slug}"


def parse_listing_for_articles(markdown_content: str) -> list[ArticleInfo]:
    """
    Parse blog listing markdown for article info.

    Expected format (from firecrawl scrape of /blog):
    - Article links with dates in nearby text
    - Pattern: [Title](/blog/slug) ... date info
    """
    articles = []

    # Pattern to find article links and nearby dates
    # The listing usually shows articles with dates like "Nov 22, 2025" or "December 2025"
    # Handles both relative paths (/blog/slug) and full URLs (https://...milanjovanovic.tech/blog/slug)
    link_pattern = re.compile(
        r'\[([^\]]+)\]\(((?:https?://(?:www\.)?milanjovanovic\.tech)?/blog/[a-z0-9-]+)\)',
        re.IGNORECASE
    )

    # Date patterns near links
    date_patterns = [
        re.compile(r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}', re.IGNORECASE),
        re.compile(r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}', re.IGNORECASE),
        re.compile(r'\d{4}-\d{2}-\d{2}'),
    ]

    # Split content into sections (usually by article)
    lines = markdown_content.split('\n')

    for i, line in enumerate(lines):
        # Find article links
        for match in link_pattern.finditer(line):
            title = match.group(1)
            path_or_url = match.group(2)
            slug = path_or_url.split('/')[-1]
            # Handle both full URLs and relative paths
            if path_or_url.startswith('http'):
                url = path_or_url
            else:
                url = f"https://www.milanjovanovic.tech{path_or_url}"

            # Look for date in FOLLOWING lines only (date appears after title in listing)
            context = '\n'.join(lines[i:min(len(lines), i+4)])

            article_date = None
            for date_pattern in date_patterns:
                date_match = date_pattern.search(context)
                if date_match:
                    parsed = parse_date(date_match.group(0))
                    if parsed:
                        article_date = parsed
                        break

            articles.append(ArticleInfo(
                url=url,
                slug=slug,
                title=title,
                date=article_date,
            ))

    return articles


def check_new_articles(
    listing_content: str,
    months: int = ROLLING_WINDOW_MONTHS,
    since: Optional[str] = None,
    force: bool = False,
    verbose: bool = False,
) -> dict:
    """
    Check for new articles that need scraping.

    Args:
        listing_content: Markdown content from blog listing page
        months: Rolling window in months (default: 6)
        since: Optional fixed date override (YYYY-MM-DD)
        force: Include existing articles for re-scraping (with content_hash for comparison)
        verbose: Print detailed output

    Returns:
        dict with 'to_scrape', 'existing', 'too_old', 'stats'
        In force mode, 'to_scrape' includes existing articles with content_hash for comparison.
    """
    manager = IndexManager()
    cutoff = get_cutoff_date(since=since, months=months)

    # Parse listing for articles
    articles = parse_listing_for_articles(listing_content)

    # Check against index and date filter
    to_scrape = []
    existing = []
    too_old = []
    no_date = []

    for article in articles:
        doc_id = slug_to_doc_id(article.slug)
        indexed_entry = manager.get(doc_id)

        # Check date first (applies to both new and force mode)
        if article.date is None:
            no_date.append(article)
            continue

        if article.date < cutoff:
            too_old.append(article)
            continue

        article.within_date_range = True

        # Check if already in index
        if indexed_entry:
            article.in_index = True
            article.content_hash = indexed_entry.content_hash
            existing.append(article)
            # In force mode, also add to scrape list (for re-check)
            if force:
                to_scrape.append(article)
        else:
            # New article - add to scrape list
            to_scrape.append(article)

    result = {
        'to_scrape': [
            {
                'url': a.url,
                'slug': a.slug,
                'title': a.title,
                'date': a.date.isoformat() if a.date else None,
                'in_index': a.in_index,
                'content_hash': a.content_hash,  # For force mode comparison
            }
            for a in to_scrape
        ],
        'existing': [
            {
                'slug': a.slug,
                'content_hash': a.content_hash,
            }
            for a in existing
        ],
        'too_old': [a.slug for a in too_old],
        'no_date': [a.slug for a in no_date],
        'stats': {
            'total_found': len(articles),
            'to_scrape': len(to_scrape),
            'already_indexed': len(existing),
            'before_cutoff': len(too_old),
            'missing_date': len(no_date),
            'cutoff_date': cutoff.date().isoformat(),
            'force_mode': force,
        },
    }

    if verbose:
        print(f"Cutoff date: {cutoff.date()}")
        print(f"Force mode: {force}")
        print(f"Total articles found: {len(articles)}")
        print(f"Already indexed: {len(existing)}")
        print(f"Before cutoff: {len(too_old)}")
        print(f"Missing date: {len(no_date)}")
        print(f"To scrape: {len(to_scrape)}")
        print()

        if to_scrape:
            print("Articles to scrape:")
            for a in to_scrape:
                date_str = a.date.date().isoformat() if a.date else 'unknown'
                status = "(re-check)" if a.in_index else "(new)"
                print(f"  [{date_str}] {a.title} {status}")
                print(f"           {a.url}")
                if a.content_hash:
                    print(f"           hash: {a.content_hash}")

    return result


def main():
    parser = argparse.ArgumentParser(
        description='Check for new Milan Jovanovic blog articles to scrape',
        epilog="""
Examples:
  # Check for new articles (default: November 2025+)
  python check_new_articles.py listing.md

  # Force mode - include all articles for re-check
  python check_new_articles.py listing.md --force

  # Output as JSON for programmatic use
  python check_new_articles.py listing.md --json

  # Pipe from stdin
  cat listing.md | python check_new_articles.py --json
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument(
        'listing_file',
        nargs='?',
        help='Path to listing page markdown (or read from stdin)',
    )
    parser.add_argument(
        '--months',
        type=int,
        default=ROLLING_WINDOW_MONTHS,
        help=f'Rolling window in months (default: {ROLLING_WINDOW_MONTHS})',
    )
    parser.add_argument(
        '--since',
        help='Fixed cutoff date (YYYY-MM-DD)',
    )
    parser.add_argument(
        '--force',
        action='store_true',
        help='Include existing articles for re-scraping (returns content_hash for comparison)',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON',
    )
    parser.add_argument(
        '--urls-only',
        action='store_true',
        help='Output only URLs of articles to scrape (one per line)',
    )

    args = parser.parse_args()

    # Read listing content
    if args.listing_file:
        with open(args.listing_file, 'r', encoding='utf-8') as f:
            content = f.read()
    else:
        content = sys.stdin.read()

    result = check_new_articles(
        content,
        months=args.months,
        since=args.since,
        force=args.force,
        verbose=args.verbose and not args.json and not args.urls_only,
    )

    if args.json:
        print(json.dumps(result, indent=2))
    elif args.urls_only:
        for article in result['to_scrape']:
            print(article['url'])
    elif not args.verbose:
        # Default: simple summary
        stats = result['stats']
        mode = "(force mode)" if stats['force_mode'] else ""
        print(f"Found {stats['to_scrape']} articles to scrape {mode} (cutoff: {stats['cutoff_date']})")
        for article in result['to_scrape']:
            status = "(re-check)" if article.get('in_index') else "(new)"
            print(f"  {article['url']} {status}")


if __name__ == '__main__':
    main()
