#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrape_blog.py - Milan Jovanovic blog scraper.

Scrapes blog articles with:
- Pagination support
- Date filtering (November 2025+ by default)
- Content cleanup (removes promotional sections)
- Idempotent operations (skip existing, content hash)
"""

import argparse
import hashlib
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Optional
from urllib.parse import urljoin, urlparse

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bootstrap import skill_dir
from utils.content_cleaner import MilanContentCleaner
from utils.date_filter import (
    DOTNET_10_RELEASE,
    extract_date_from_metadata,
    get_cutoff_date,
    should_include_article,
)
from utils.config_helpers import config


class BlogScraper:
    """
    Scraper for Milan Jovanovic's blog.

    Features:
    - Pagination crawling
    - Date filtering
    - Content cleanup
    - Idempotent operations
    """

    def __init__(
        self,
        min_date: Optional[datetime] = None,
        skip_existing: bool = True,
        dry_run: bool = False,
        limit: Optional[int] = None,
        verbose: bool = False,
    ):
        self.min_date = min_date or DOTNET_10_RELEASE
        self.skip_existing = skip_existing
        self.dry_run = dry_run
        self.limit = limit
        self.verbose = verbose

        self.cleaner = MilanContentCleaner()
        self.skill_root = skill_dir
        self.canonical_dir = self.skill_root / 'canonical'
        self.index_path = self.canonical_dir / 'index.json'

        # Load sources configuration
        sources_path = self.skill_root / 'references' / 'sources.json'
        with open(sources_path, 'r', encoding='utf-8') as f:
            self.sources = json.load(f)

        # Load existing index
        self.index = self._load_index()

        # Stats
        self.stats = {
            'pages_crawled': 0,
            'articles_found': 0,
            'articles_scraped': 0,
            'articles_skipped': 0,
            'articles_filtered': 0,
            'errors': 0,
        }

    def _load_index(self) -> dict:
        """Load existing index or create empty one."""
        if self.index_path.exists():
            with open(self.index_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}

    def _save_index(self) -> None:
        """Save index to disk."""
        if self.dry_run:
            return

        self.canonical_dir.mkdir(parents=True, exist_ok=True)
        with open(self.index_path, 'w', encoding='utf-8') as f:
            json.dump(self.index, f, indent=2, ensure_ascii=False)

    def _generate_doc_id(self, url: str) -> str:
        """Generate doc_id from URL."""
        parsed = urlparse(url)
        path = parsed.path.strip('/')
        # Convert path to doc_id format
        slug = path.replace('/', '-')
        return f"milanjovanovic-tech-{slug}"

    def _content_hash(self, content: str) -> str:
        """Generate SHA256 hash of content."""
        return f"sha256:{hashlib.sha256(content.encode('utf-8')).hexdigest()[:16]}"

    def _extract_article_links(self, html: str, base_url: str) -> list[str]:
        """Extract article links from blog listing page."""
        # Pattern for article links in the blog listing
        # Milan's blog uses /blog/slug pattern
        pattern = r'href=["\'](/blog/[^/"\']+)["\']'
        matches = re.findall(pattern, html)

        # Deduplicate and convert to full URLs
        seen = set()
        links = []
        for path in matches:
            if path not in seen and not path.startswith('/blog/p/'):
                seen.add(path)
                links.append(urljoin(base_url, path))

        return links

    def _fetch_url(self, url: str) -> Optional[dict]:
        """
        Fetch URL using Firecrawl MCP.

        Returns dict with 'markdown', 'metadata', 'html' keys.
        """
        # This is a placeholder - actual implementation will use Firecrawl
        # When invoked by Claude, this will be replaced with actual MCP calls
        print(f"[FETCH] {url}")
        return None

    def _scrape_article(self, url: str) -> Optional[dict]:
        """
        Scrape a single article.

        Returns article data dict or None if skipped/failed.
        """
        doc_id = self._generate_doc_id(url)

        # Check if already scraped
        if self.skip_existing and doc_id in self.index:
            if self.verbose:
                print(f"[SKIP] Already indexed: {url}")
            self.stats['articles_skipped'] += 1
            return None

        # Fetch article
        result = self._fetch_url(url)
        if not result:
            self.stats['errors'] += 1
            return None

        # Extract metadata
        metadata = result.get('metadata', {})
        published_at = extract_date_from_metadata(metadata)

        # Check date filter
        if not should_include_article(published_at, self.min_date):
            if self.verbose:
                date_str = published_at.date() if published_at else 'unknown'
                print(f"[FILTER] Before cutoff ({date_str}): {url}")
            self.stats['articles_filtered'] += 1
            return None

        # Get and clean content
        content = result.get('markdown', '')
        cleaned = self.cleaner.clean_content(content, url)

        # Generate content hash
        content_hash = self._content_hash(cleaned.content)

        # Check if content unchanged (even if re-scraping)
        if doc_id in self.index:
            if self.index[doc_id].get('content_hash') == content_hash:
                if self.verbose:
                    print(f"[UNCHANGED] Content hash match: {url}")
                self.stats['articles_skipped'] += 1
                return None

        # Extract title from content
        title_match = re.match(r'^#\s+(.+)$', cleaned.content, re.MULTILINE)
        title = title_match.group(1) if title_match else metadata.get('title', 'Untitled')

        # Extract description (first paragraph after title)
        desc_match = re.search(r'^#[^\n]+\n+([^\n#]+)', cleaned.content)
        description = desc_match.group(1).strip()[:200] if desc_match else ''

        # Build article data
        article = {
            'doc_id': doc_id,
            'title': title,
            'description': description,
            'source_url': url,
            'published_at': published_at.isoformat() if published_at else None,
            'last_fetched': datetime.now(timezone.utc).isoformat(),
            'content_hash': content_hash,
            'content': cleaned.content,
            'metadata': {
                'sections_removed': cleaned.sections_removed,
                'inline_removals': cleaned.inline_removals,
            },
        }

        self.stats['articles_scraped'] += 1
        return article

    def _save_article(self, article: dict) -> Path:
        """Save article to canonical storage."""
        if self.dry_run:
            print(f"[DRY-RUN] Would save: {article['doc_id']}")
            return Path()

        # Create output directory
        output_dir = self.canonical_dir / 'milanjovanovic-tech' / 'blog'
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate filename from URL slug
        slug = article['doc_id'].replace('milanjovanovic-tech-blog-', '')
        file_path = output_dir / f"{slug}.md"

        # Write content with frontmatter
        frontmatter = f"""---
doc_id: {article['doc_id']}
title: "{article['title'].replace('"', '\\"')}"
source_url: {article['source_url']}
published_at: {article['published_at']}
last_fetched: {article['last_fetched']}
content_hash: {article['content_hash']}
---

"""
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(frontmatter + article['content'])

        # Update index
        self.index[article['doc_id']] = {
            'doc_id': article['doc_id'],
            'title': article['title'],
            'description': article['description'],
            'path': str(file_path.relative_to(self.canonical_dir)),
            'source_url': article['source_url'],
            'published_at': article['published_at'],
            'last_fetched': article['last_fetched'],
            'content_hash': article['content_hash'],
        }

        return file_path

    def scrape(self) -> dict:
        """
        Run the scraper.

        Returns statistics dict.
        """
        print(f"\n{'='*60}")
        print("Milan Jovanovic Blog Scraper")
        print(f"{'='*60}")
        print(f"Min date: {self.min_date.date()}")
        print(f"Skip existing: {self.skip_existing}")
        print(f"Dry run: {self.dry_run}")
        if self.limit:
            print(f"Limit: {self.limit} articles")
        print(f"{'='*60}\n")

        source = self.sources[0]  # We only have one source
        base_url = source['base_url']
        max_pages = source['max_pages']
        rate_limit = source.get('rate_limit_ms', 1000) / 1000

        all_article_urls = []

        # Crawl pagination pages to collect article URLs
        for page in range(1, max_pages + 1):
            if page == 1:
                page_url = base_url
            else:
                page_url = f"{base_url}/p/{page}"

            print(f"[PAGE] Crawling page {page}: {page_url}")
            self.stats['pages_crawled'] += 1

            result = self._fetch_url(page_url)
            if not result:
                print(f"[ERROR] Failed to fetch page {page}")
                break

            html = result.get('html', '')
            links = self._extract_article_links(html, base_url)

            if not links:
                print(f"[END] No articles found on page {page}, stopping")
                break

            all_article_urls.extend(links)
            self.stats['articles_found'] += len(links)

            if self.limit and len(all_article_urls) >= self.limit:
                all_article_urls = all_article_urls[:self.limit]
                break

            time.sleep(rate_limit)

        print(f"\n[FOUND] {len(all_article_urls)} article URLs\n")

        # Scrape each article
        for i, url in enumerate(all_article_urls, 1):
            print(f"[{i}/{len(all_article_urls)}] {url}")

            article = self._scrape_article(url)
            if article:
                path = self._save_article(article)
                if not self.dry_run:
                    print(f"  -> Saved: {path}")

            time.sleep(rate_limit)

        # Save updated index
        self._save_index()

        # Print summary
        print(f"\n{'='*60}")
        print("Scrape Complete")
        print(f"{'='*60}")
        print(f"Pages crawled: {self.stats['pages_crawled']}")
        print(f"Articles found: {self.stats['articles_found']}")
        print(f"Articles scraped: {self.stats['articles_scraped']}")
        print(f"Articles skipped: {self.stats['articles_skipped']}")
        print(f"Articles filtered: {self.stats['articles_filtered']}")
        print(f"Errors: {self.stats['errors']}")
        print(f"{'='*60}\n")

        return self.stats


def main():
    """CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Scrape Milan Jovanovic blog articles',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run with limit
  python scrape_blog.py --dry-run --limit 3

  # Scrape new articles only
  python scrape_blog.py --skip-existing

  # Force re-scrape all
  python scrape_blog.py --no-skip-existing

  # Custom date filter
  python scrape_blog.py --since 2025-12-01
        """,
    )

    parser.add_argument(
        '--since',
        type=str,
        default=None,
        help='Minimum article date (YYYY-MM-DD). Default: 2025-11-01',
    )
    parser.add_argument(
        '--skip-existing',
        action='store_true',
        default=True,
        help='Skip already indexed articles (default)',
    )
    parser.add_argument(
        '--no-skip-existing',
        action='store_true',
        help='Re-scrape all articles',
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be scraped without saving',
    )
    parser.add_argument(
        '--limit',
        type=int,
        default=None,
        help='Limit number of articles to scrape',
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Verbose output',
    )

    args = parser.parse_args()

    # Parse date
    min_date = get_cutoff_date(args.since)

    # Handle skip_existing flag
    skip_existing = not args.no_skip_existing

    # Create and run scraper
    scraper = BlogScraper(
        min_date=min_date,
        skip_existing=skip_existing,
        dry_run=args.dry_run,
        limit=args.limit,
        verbose=args.verbose,
    )

    stats = scraper.scrape()

    # Exit with error if any failures
    if stats['errors'] > 0:
        sys.exit(1)


if __name__ == '__main__':
    main()
