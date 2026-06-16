#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scrape_docs.py - Fetch and parse Duende documentation from llms-full.txt

This scraper is designed for Duende's documentation format which provides
all docs in a single pre-rendered llms-full.txt file, making scraping
much simpler than URL-by-URL approaches.

Usage:
    # Scrape all Duende documentation
    python scrape_docs.py

    # Scrape with custom base directory
    python scrape_docs.py --base-dir /path/to/canonical

    # Test with limit
    python scrape_docs.py --limit 5

Dependencies:
    pip install requests pyyaml
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import argparse
import hashlib
import os
import threading
import time
from datetime import datetime, timezone
from urllib.parse import urlparse

from utils.script_utils import configure_utf8_output, format_duration
from utils.path_config import get_base_dir, get_index_path
from utils.config_helpers import (
    get_scraper_user_agent,
    get_http_timeout,
    get_http_max_retries,
    get_http_initial_retry_delay,
)
from utils.http_utils import fetch_with_retry
configure_utf8_output()

# Ensure unbuffered output for real-time streaming
if sys.stdout.isatty():
    sys.stdout.reconfigure(line_buffering=True)
else:
    sys.stdout.reconfigure(line_buffering=True)

# Thread-safe print helper
_print_lock = threading.Lock()

def safe_print(*args, **kwargs):
    """Thread-safe print that flushes immediately for real-time output"""
    with _print_lock:
        print(*args, **kwargs, flush=True)

from utils.logging_utils import get_or_setup_logger

# Get source name from environment
_source_name = os.environ.get('DUENDE_DOCS_SOURCE_NAME', '')
_log_prefix = f"[{_source_name}] " if _source_name else ""

logger = get_or_setup_logger(__file__, log_category="scrape")

from utils.script_utils import ensure_yaml_installed

try:
    import requests
except ImportError as e:
    print(f"Missing dependency: {e}")
    print("Install with: pip install requests")
    sys.exit(1)

yaml = ensure_yaml_installed()

# Import the Duende-specific parser
from llms_full_parser import LlmsFullParser, SitemapUrlResolver, DuendePage, url_to_local_path

# Import index_manager for large file support
try:
    from management.index_manager import IndexManager
except ImportError:
    IndexManager = None

# Import metadata extractor
try:
    from management.extract_metadata import MetadataExtractor
except ImportError:
    MetadataExtractor = None


# Default source URLs
DEFAULT_LLMS_FULL_URL = 'https://docs.duendesoftware.com/llms-full.txt'
DEFAULT_SITEMAP_URL = 'https://docs.duendesoftware.com/sitemap-0.xml'
DEFAULT_DOMAIN_DIR = 'duendesoftware-com'

# Smart quote / typographic character -> ASCII mapping
SMART_QUOTE_MAP = {
    '\u201c': '"',   # left double quote
    '\u201d': '"',   # right double quote
    '\u2018': "'",   # left single quote
    '\u2019': "'",   # right single quote
    '\u2013': '-',   # en dash
    '\u2014': '--',  # em dash
    '\u2026': '...', # ellipsis
}


class DuendeDocScraper:
    """Documentation scraper for Duende's llms-full.txt format"""

    def __init__(self, base_output_dir: Path | None = None, domain_dir: str = DEFAULT_DOMAIN_DIR):
        """
        Initialize scraper

        Args:
            base_output_dir: Base directory for canonical storage. If None, uses config default.
            domain_dir: Subdirectory for domain (default: duendesoftware-com)
        """
        self.base_output_dir = base_output_dir if base_output_dir else get_base_dir()
        self.domain_dir = domain_dir
        self.index_path = get_index_path(self.base_output_dir)

        # Session for HTTP requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': get_scraper_user_agent()
        })

        # Initialize parser
        self.parser = LlmsFullParser()

        # Initialize index manager if available
        if IndexManager:
            self.index_manager = IndexManager(base_output_dir)
        else:
            self.index_manager = None

        # Statistics
        self.stats = {
            'total_pages': 0,
            'saved_pages': 0,
            'skipped_pages': 0,
            'failed_pages': 0,
            'categories': {},
        }

    @staticmethod
    def _fix_encoding(content: str) -> str:
        """Fix double-encoded UTF-8 and normalize smart quotes to ASCII.

        Applied per-page to avoid a single non-Latin-1 character causing the
        entire fix to be skipped. Each page's content is independently decoded.
        """
        # Step 1: Reverse double-encoding (UTF-8 -> Latin-1 -> UTF-8)
        try:
            content = content.encode('latin-1').decode('utf-8')
        except (UnicodeDecodeError, UnicodeEncodeError):
            pass  # Not double-encoded, continue with normalization

        # Step 2: Normalize smart quotes/dashes to ASCII
        for char, replacement in SMART_QUOTE_MAP.items():
            content = content.replace(char, replacement)
        return content

    def fetch_sitemap_urls(self, url: str = DEFAULT_SITEMAP_URL) -> list[str]:
        """Fetch sitemap XML and extract URLs for URL resolution.

        Args:
            url: URL to sitemap XML file

        Returns:
            List of URLs from sitemap, empty list on failure (graceful degradation)
        """
        import xml.etree.ElementTree as ET

        print(f"Fetching sitemap: {url}")
        try:
            timeout = get_http_timeout()
            max_retries = get_http_max_retries()
            initial_delay = get_http_initial_retry_delay()

            response = fetch_with_retry(
                url,
                max_retries=max_retries,
                initial_delay=initial_delay,
                timeout=timeout,
                session=self.session
            )

            root = ET.fromstring(response.text)
            # Handle namespace: sitemap XML uses xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
            ns = {'sm': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
            urls = [
                loc.text
                for loc in root.findall('.//sm:loc', ns)
                if loc.text
            ]
            # Fallback: try without namespace
            if not urls:
                urls = [
                    loc.text
                    for loc in root.findall('.//loc')
                    if loc.text
                ]
            print(f"  Found {len(urls)} URLs in sitemap")
            return urls

        except Exception as e:
            print(f"  Warning: Could not fetch sitemap ({e}), URL resolution will use fallback")
            return []

    def fetch_llms_full(self, url: str = DEFAULT_LLMS_FULL_URL) -> str | None:
        """
        Fetch the llms-full.txt content from Duende's documentation site.

        Args:
            url: URL to llms-full.txt file

        Returns:
            Content string or None if fetch failed
        """
        print(f"Fetching: {url}")

        try:
            timeout = get_http_timeout()
            max_retries = get_http_max_retries()
            initial_delay = get_http_initial_retry_delay()

            response = fetch_with_retry(
                url,
                max_retries=max_retries,
                initial_delay=initial_delay,
                timeout=timeout,
                session=self.session
            )

            content = response.text
            # Smart quote normalization only at global level;
            # double-encoding fix is applied per-page in save_page()
            # to avoid a single non-Latin-1 char skipping all pages.
            for char, replacement in SMART_QUOTE_MAP.items():
                content = content.replace(char, replacement)
            print(f"  Fetched {len(content):,} characters")
            return content

        except requests.HTTPError as e:
            status_code = e.response.status_code if e.response else None
            print(f"  HTTP error {status_code}: {url}")
            logger.log_error(f"HTTP error fetching llms-full.txt", error=e)
            return None

        except (requests.ConnectionError, requests.Timeout, requests.RequestException) as e:
            error_type = type(e).__name__
            print(f"  {error_type}: {url}")
            logger.log_error(f"Error fetching llms-full.txt", error=e)
            return None

    def calculate_hash(self, content: str) -> str:
        """Calculate SHA-256 hash of content"""
        hash_obj = hashlib.sha256(content.encode('utf-8'))
        return f"sha256:{hash_obj.hexdigest()}"

    def add_frontmatter(self, page: DuendePage) -> str:
        """
        Add YAML frontmatter to page content.

        Args:
            page: DuendePage object

        Returns:
            Content with frontmatter prepended
        """
        content_hash = self.calculate_hash(page.content)

        # Note: last_fetched is stored ONLY in index.yaml, not in frontmatter
        # This prevents git noise from timestamp-only changes
        frontmatter = {
            'title': page.title,
            'source_url': page.source_url,
            'source_type': 'llms-full-txt',
            'content_hash': content_hash,
        }

        if page.category:
            frontmatter['category'] = page.category

        if page.doc_id:
            frontmatter['doc_id'] = page.doc_id

        yaml_frontmatter = yaml.dump(frontmatter, default_flow_style=False, sort_keys=False, allow_unicode=True)

        return f"---\n{yaml_frontmatter}---\n\n{page.content}"

    def should_skip_page(self, output_path: Path, page: DuendePage, force: bool = False) -> bool:
        """
        Check if page should be skipped (already exists with matching hash).

        Args:
            output_path: Path where file would be saved
            page: DuendePage to check
            force: If True, never skip

        Returns:
            True if page should be skipped
        """
        if force:
            return False

        if not output_path.exists():
            return False

        try:
            existing_content = output_path.read_text(encoding='utf-8')
            if not existing_content.startswith('---'):
                return False

            frontmatter_end = existing_content.find('---', 3)
            if frontmatter_end == -1:
                return False

            frontmatter_text = existing_content[3:frontmatter_end].strip()
            frontmatter = yaml.safe_load(frontmatter_text)

            existing_hash = frontmatter.get('content_hash')
            if not existing_hash:
                return False

            new_hash = self.calculate_hash(page.content)
            if existing_hash == new_hash:
                return True

            return False

        except Exception as e:
            logger.warning(f"Error checking skip status for {output_path}: {e}")
            return False

    def save_page(self, page: DuendePage, force: bool = False) -> dict | None:
        """
        Save a single page to the canonical directory.

        Args:
            page: DuendePage to save
            force: If True, overwrite even if hash matches

        Returns:
            Metadata dict if saved, None if skipped or failed
        """
        # Determine output path using doc_id (URL-path-based) for full hierarchy
        output_dir = self.base_output_dir / self.domain_dir

        if page.doc_id:
            # doc_id is now URL-path-based (e.g., "bff/getting-started")
            # Use it directly as the relative path to preserve hierarchy
            output_path = output_dir / (page.doc_id + '.md')
        elif page.category:
            filename = self.parser._title_to_slug(page.title) + '.md'
            output_path = output_dir / page.category / filename
        else:
            filename = self.parser._title_to_slug(page.title) + '.md'
            output_path = output_dir / filename

        # Fix per-page encoding (double-encoded UTF-8)
        page.content = self._fix_encoding(page.content)

        # Check if should skip
        if self.should_skip_page(output_path, page, force):
            self.stats['skipped_pages'] += 1
            return None

        # Create content with frontmatter
        final_content = self.add_frontmatter(page)

        # Ensure directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Ensure content ends with newline
        if not final_content.endswith('\n'):
            final_content += '\n'

        # Write file
        try:
            with open(output_path, 'w', encoding='utf-8', newline='\n') as f:
                f.write(final_content)

            safe_print(f"  Saved: {output_path.relative_to(self.base_output_dir)}")
            self.stats['saved_pages'] += 1

            # Track category stats
            cat = page.category or 'uncategorized'
            self.stats['categories'][cat] = self.stats['categories'].get(cat, 0) + 1

            # Build metadata for index
            try:
                relative_to_base = output_path.relative_to(self.base_output_dir)
                path_normalized = str(relative_to_base).replace('\\', '/')
            except ValueError:
                path_normalized = str(output_path).replace('\\', '/')

            metadata = {
                'path': path_normalized,
                'url': page.source_url,
                'title': page.title,
                'hash': self.calculate_hash(final_content),
                'last_fetched': datetime.now(timezone.utc).strftime('%Y-%m-%d'),
                'source_type': 'llms-full-txt',
            }

            if page.category:
                metadata['category'] = page.category

            if page.doc_id:
                metadata['doc_id'] = page.doc_id

            # Extract additional metadata if extractor available
            if MetadataExtractor:
                try:
                    extractor = MetadataExtractor(output_path, page.source_url)
                    extracted = extractor.extract_all()
                    metadata.update(extracted)
                except Exception:
                    pass

            return metadata

        except Exception as e:
            logger.log_error(f"Failed to save {output_path}", error=e)
            self.stats['failed_pages'] += 1
            return None

    def update_index(self, doc_id: str, metadata: dict) -> None:
        """
        Update index.yaml with document metadata.

        Args:
            doc_id: Document identifier
            metadata: Metadata dictionary
        """
        if self.index_manager:
            if not self.index_manager.update_entry(doc_id, metadata):
                logger.warning(f"Failed to update index entry: {doc_id}")
        else:
            # Direct YAML update (fallback)
            lock_file = self.index_path.parent / '.index.lock'
            start_time = time.time()
            timeout = 30.0

            while time.time() - start_time < timeout:
                try:
                    fd = os.open(str(lock_file), os.O_CREAT | os.O_EXCL | os.O_WRONLY)
                    os.close(fd)
                    break
                except OSError:
                    time.sleep(0.1)
                    continue
            else:
                logger.warning("Could not acquire index lock")
                return

            try:
                if self.index_path.exists():
                    with open(self.index_path, 'r', encoding='utf-8') as f:
                        index = yaml.safe_load(f) or {}
                else:
                    index = {}

                index[doc_id] = metadata

                with open(self.index_path, 'w', encoding='utf-8') as f:
                    yaml.dump(index, f, default_flow_style=False, sort_keys=False, allow_unicode=True)
            finally:
                try:
                    if lock_file.exists():
                        lock_file.unlink()
                except Exception:
                    pass

    def scrape(self, url: str = DEFAULT_LLMS_FULL_URL, limit: int | None = None,
               force: bool = False, skip_existing: bool = True) -> int:
        """
        Scrape all documentation from llms-full.txt.

        Args:
            url: URL to llms-full.txt file
            limit: Maximum number of pages to process (for testing)
            force: If True, overwrite all files regardless of hash
            skip_existing: If True, skip files with matching hash

        Returns:
            Number of pages successfully processed
        """
        scrape_start_time = time.time()

        # Fetch the llms-full.txt content
        content = self.fetch_llms_full(url)
        if not content:
            print("Failed to fetch llms-full.txt")
            return 0

        # Fetch sitemap for URL resolution
        sitemap_urls = self.fetch_sitemap_urls()
        if sitemap_urls:
            resolver = SitemapUrlResolver()
            resolver.load_from_urls(sitemap_urls)
            self.parser.url_resolver = resolver
            print(f"  URL resolver loaded with {len(sitemap_urls)} sitemap URLs")

        # Parse the content
        print("\nParsing documentation...")
        raw_pages = list(self.parser.parse_stream(content))
        print(f"  Found {len(raw_pages)} documentation pages")

        # Deduplicate pages with the same source_url
        seen_urls: dict[str, DuendePage] = {}
        pages: list[DuendePage] = []
        duplicates = 0
        for page in raw_pages:
            url_key = page.source_url or ''
            if url_key in seen_urls:
                existing = seen_urls[url_key]
                # Prefer the version with a category
                if page.category and not existing.category:
                    pages = [p for p in pages if p is not existing]
                    pages.append(page)
                    seen_urls[url_key] = page
                    safe_print(f"  Dedup: replaced uncategorized '{existing.title}' "
                               f"with categorized '{page.title}' ({url_key})")
                else:
                    safe_print(f"  Dedup: skipped duplicate '{page.title}' ({url_key})")
                duplicates += 1
            else:
                seen_urls[url_key] = page
                pages.append(page)

        if duplicates:
            print(f"  Deduplicated {duplicates} pages with duplicate source_urls")

        self.stats['total_pages'] = len(pages)
        print(f"  Unique pages: {len(pages)}")

        # Show category breakdown
        categories = self.parser.get_categories(content)
        print("\n  Categories:")
        for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
            print(f"    {cat or 'uncategorized'}: {count}")

        # Apply limit if specified
        if limit:
            pages = pages[:limit]
            print(f"\n  Limiting to first {limit} pages (test mode)")

        # Process each page
        print(f"\nSaving pages to: {self.base_output_dir / self.domain_dir}")
        print("=" * 60)

        for i, page in enumerate(pages, 1):
            print(f"\n[{i}/{len(pages)}] {page.title}")

            # Save the page
            metadata = self.save_page(page, force=force)

            # Update index if saved
            if metadata:
                doc_id = page.doc_id or self.parser._generate_doc_id(page.title, page.category, page.source_url)
                self.update_index(doc_id, metadata)

        # Print summary
        total_time = time.time() - scrape_start_time
        throughput = len(pages) / total_time if total_time > 0 else 0

        print(f"\n{'='*60}")
        print(f"Scraping Summary:")
        print(f"{'='*60}")
        print(f"  Total pages:    {self.stats['total_pages']}")
        print(f"  Saved:          {self.stats['saved_pages']}")
        print(f"  Skipped:        {self.stats['skipped_pages']}")
        if self.stats['failed_pages'] > 0:
            print(f"  Failed:         {self.stats['failed_pages']}")
        print(f"{'='*60}")
        print(f"  Total time:     {format_duration(total_time)}")
        print(f"  Throughput:     {throughput:.1f} pages/sec")
        print(f"{'='*60}")

        if self.stats['categories']:
            print("\n  Pages by category:")
            for cat, count in sorted(self.stats['categories'].items(), key=lambda x: x[1], reverse=True):
                print(f"    {cat}: {count}")

        return self.stats['saved_pages']


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Scrape Duende documentation from llms-full.txt',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Scrape all Duende documentation
  python scrape_docs.py

  # Scrape with custom base directory
  python scrape_docs.py --base-dir /path/to/canonical

  # Test with limit
  python scrape_docs.py --limit 5

  # Force re-scrape all (ignore existing)
  python scrape_docs.py --force
        """
    )

    # Source URL
    parser.add_argument('--url', default=DEFAULT_LLMS_FULL_URL,
                        help=f'URL to llms-full.txt (default: {DEFAULT_LLMS_FULL_URL})')

    # Output
    from utils.cli_utils import add_base_dir_argument, resolve_base_dir_from_args
    add_base_dir_argument(parser)

    # Options
    parser.add_argument('--limit', type=int,
                        help='Limit number of pages to process (for testing)')
    parser.add_argument('--force', action='store_true',
                        help='Force overwrite all files regardless of hash')
    parser.add_argument('--no-skip', action='store_true',
                        help='Do not skip files with matching hash')

    args = parser.parse_args()

    # Print dev/prod mode banner for visibility
    if not _source_name:
        from utils.dev_mode import print_mode_banner
        from utils.path_config import get_base_dir
        print_mode_banner(logger)
        logger.info(f"Canonical dir: {get_base_dir()}")

    start_context = {
        'source': 'llms_full_txt',
        'url': args.url,
        'base_dir': args.base_dir,
        'limit': args.limit,
        'force': args.force
    }
    if _source_name:
        start_context['source_name'] = _source_name
    logger.start(start_context)

    exit_code = 0
    try:
        base_dir = resolve_base_dir_from_args(args)
        base_dir.mkdir(parents=True, exist_ok=True)

        print(f"Using base directory: {base_dir}")
        print(f"   (Absolute path: {base_dir.absolute()})")

        scraper = DuendeDocScraper(base_dir)

        success_count = scraper.scrape(
            url=args.url,
            limit=args.limit,
            force=args.force,
            skip_existing=not args.no_skip
        )

        print(f"\n{'='*60}")
        print(f"Scraping complete: {success_count} document(s) saved")

        # Show output stats
        output_dir = base_dir / DEFAULT_DOMAIN_DIR
        if output_dir.exists():
            md_files = list(output_dir.glob("**/*.md"))
            total_size = sum(f.stat().st_size for f in md_files)
            size_mb = total_size / 1024 / 1024
            print(f"Total files: {len(md_files)}")
            print(f"Total size: {size_mb:.2f} MB")
            logger.track_metric('total_files', len(md_files))
            logger.track_metric('total_size_mb', size_mb)

        logger.track_metric('success_count', success_count)

        summary = {
            'success_count': success_count,
            'source': 'llms_full_txt',
            'url': args.url
        }
        if _source_name:
            summary['source_name'] = _source_name

        logger.end(exit_code=exit_code, summary=summary)

    except SystemExit:
        raise
    except Exception as e:
        logger.log_error("Fatal error in scrape_docs", error=e)
        exit_code = 1
        logger.end(exit_code=exit_code)
        sys.exit(exit_code)


if __name__ == '__main__':
    main()
