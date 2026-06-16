#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
llms_full_parser.py - Parse Duende's llms-full.txt format.

This module provides a parser for Duende's pre-rendered llms-full.txt documentation format.
The format is different from cursor-ecosystem in that it uses:
- `-----` as page separators
- `# Title` headers for each page
- Optional `Source: URL` lines (may not be present)
- Content is already markdown (no HTML conversion needed)

Usage:
    from core.llms_full_parser import LlmsFullParser, DuendePage

    parser = LlmsFullParser()
    for page in parser.parse_stream(content):
        print(f"{page.title}: {len(page.content)} chars")
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import re
from dataclasses import dataclass, field
from typing import Generator
from urllib.parse import quote


@dataclass
class DuendePage:
    """Single page from Duende's llms-full.txt content file."""
    title: str
    content: str
    source_url: str | None = None
    category: str | None = None
    doc_id: str | None = None


# Category mappings for URL derivation
CATEGORY_URL_PATTERNS: dict[str, str] = {
    'identityserver': '/identityserver/',
    'bff': '/bff/',
    'accesstokenmanagement': '/accesstokenmanagement/',
    'identitymodel': '/identitymodel/',
    'identitymodel-oidcclient': '/identitymodel-oidcclient/',
    'introspection': '/introspection/',
    'general': '/',
}

# Title patterns that indicate specific categories
TITLE_CATEGORY_PATTERNS: list[tuple[re.Pattern, str]] = [
    (re.compile(r'identityserver', re.IGNORECASE), 'identityserver'),
    (re.compile(r'\bbff\b', re.IGNORECASE), 'bff'),
    (re.compile(r'backend.for.frontend', re.IGNORECASE), 'bff'),
    (re.compile(r'access.token.management', re.IGNORECASE), 'accesstokenmanagement'),
    (re.compile(r'identitymodel.*oidc', re.IGNORECASE), 'identitymodel-oidcclient'),
    (re.compile(r'oidc.?client', re.IGNORECASE), 'identitymodel-oidcclient'),
    (re.compile(r'identitymodel', re.IGNORECASE), 'identitymodel'),
    (re.compile(r'introspection', re.IGNORECASE), 'introspection'),
]


class SitemapUrlResolver:
    """Resolves page slugs to real URLs using sitemap data.

    Duende's sitemap contains deep hierarchical URLs like
    /identityserver/ui/server-side-sessions/inactivity-timeout/
    while the parser only has page titles. This class builds a
    slug-to-URL mapping for accurate resolution.
    """

    def __init__(self, base_url: str = 'https://docs.duendesoftware.com'):
        self.base_url = base_url.rstrip('/')
        self._slug_to_paths: dict[str, list[str]] = {}
        self._category_slug_to_path: dict[str, dict[str, str]] = {}

    def load_from_urls(self, urls: list[str]) -> None:
        """Build slug->URL mapping from sitemap URL list."""
        for url in urls:
            # Strip base URL to get path
            if url.startswith(self.base_url):
                path = url[len(self.base_url):]
            else:
                from urllib.parse import urlparse
                path = urlparse(url).path

            path = path.strip('/')
            if not path:
                continue

            segments = path.split('/')
            slug = segments[-1]  # last segment is the slug

            # Store full URL keyed by slug
            if slug not in self._slug_to_paths:
                self._slug_to_paths[slug] = []
            self._slug_to_paths[slug].append(url)

            # Store category (first segment) for disambiguation
            if len(segments) >= 1:
                category = segments[0]
                if category not in self._category_slug_to_path:
                    self._category_slug_to_path[category] = {}
                self._category_slug_to_path[category][slug] = url

    def resolve(self, slug: str, category: str | None = None) -> str | None:
        """Look up slug, use category to disambiguate. Returns full URL or None."""
        paths = self._slug_to_paths.get(slug)
        if not paths:
            return None

        # Single match - no ambiguity
        if len(paths) == 1:
            return paths[0]

        # Multiple matches - try category disambiguation
        if category and category in self._category_slug_to_path:
            cat_match = self._category_slug_to_path[category].get(slug)
            if cat_match:
                return cat_match

        # Fallback: return first match
        return paths[0]


class LlmsFullParser:
    """
    Stream parser for Duende's llms-full.txt content format.

    Duende's llms-full.txt format (pages separated by -----):
        <SYSTEM>This is the full developer documentation...</SYSTEM>
        -----
        # Page Title

        [Full markdown content of the page...]

        -----
        # Next Page Title

        [Next page content...]

    This parser is memory-efficient for large files.
    """

    # Page separator: five or more dashes
    SEPARATOR_PATTERN = re.compile(r'^-{5,}\s*$')

    # Title pattern: # Page Title (at start of line)
    TITLE_PATTERN = re.compile(r'^#\s+(.+)$')

    # Source pattern: Source: URL (optional in Duende format)
    SOURCE_PATTERN = re.compile(r'^Source:\s*(https?://\S+)\s*$', re.IGNORECASE)

    # System instruction pattern (skip these)
    SYSTEM_PATTERN = re.compile(r'^<SYSTEM>.*</SYSTEM>$', re.IGNORECASE)

    # Section anchor pattern for deriving doc_id
    SECTION_ANCHOR_PATTERN = re.compile(r'\[Section titled ["\u201c]([^"\u201d]+)["\u201d]\]\(#([^)]+)\)')

    def __init__(self, base_url: str = 'https://docs.duendesoftware.com',
                 url_resolver: SitemapUrlResolver | None = None):
        """
        Initialize parser.

        Args:
            base_url: Base URL for Duende documentation
            url_resolver: Optional SitemapUrlResolver for accurate URL mapping
        """
        self.base_url = base_url.rstrip('/')
        self.url_resolver = url_resolver

    def _detect_category(self, title: str, content: str) -> str | None:
        """
        Detect category from title or content.

        Args:
            title: Page title
            content: Page content

        Returns:
            Category string or None
        """
        # Check title patterns
        for pattern, category in TITLE_CATEGORY_PATTERNS:
            if pattern.search(title):
                return category

        # Check content for category indicators
        content_lower = content[:500].lower()  # Check first 500 chars
        for category in CATEGORY_URL_PATTERNS:
            if f'/{category}/' in content_lower:
                return category

        return None

    def _derive_url(self, title: str, category: str | None, content: str) -> str:
        """
        Derive a URL from the page title and category.

        Uses sitemap-based URL resolver when available for accurate deep URLs,
        falling back to title-based derivation.

        Args:
            title: Page title
            category: Detected category
            content: Page content (may contain URL hints)

        Returns:
            Derived URL
        """
        # Try sitemap resolver first (most accurate)
        if self.url_resolver:
            slug = self._title_to_slug(title)
            resolved = self.url_resolver.resolve(slug, category)
            if resolved:
                return resolved

        # Check for explicit URL in content (e.g., [Learn more](/path/))
        learn_more_match = re.search(r'\[Learn more\]\((/[^)]+)\)', content)
        if learn_more_match:
            path = learn_more_match.group(1)
            return f"{self.base_url}{path}"

        # Generate URL from title (fallback)
        slug = self._title_to_slug(title)

        if category:
            base_path = CATEGORY_URL_PATTERNS.get(category, '/')
            return f"{self.base_url}{base_path}{slug}/"

        return f"{self.base_url}/{slug}/"

    def _title_to_slug(self, title: str) -> str:
        """
        Convert a title to a URL slug.

        Args:
            title: Page title

        Returns:
            URL-safe slug
        """
        # Remove common suffixes
        title = re.sub(r'\s*\(.*?\)\s*$', '', title)

        # Convert to lowercase and replace spaces/special chars
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'[\s_]+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')

        return slug

    def _generate_doc_id(self, title: str, category: str | None,
                         source_url: str | None = None) -> str:
        """
        Generate a doc_id from source URL path, falling back to title+category.

        Uses the URL path to avoid collisions when multiple pages share the
        same title (e.g., multiple "Getting Started" pages in different products).

        Args:
            title: Page title
            category: Detected category
            source_url: Resolved source URL (preferred for doc_id derivation)

        Returns:
            Generated doc_id
        """
        # Prefer URL-based doc_id to avoid title collisions
        if source_url:
            from urllib.parse import urlparse
            path = urlparse(source_url).path.strip('/')
            if path:
                return path

        slug = self._title_to_slug(title)

        if category:
            return f"{category}/{slug}"

        return slug

    def parse_stream(self, content: str) -> Generator[DuendePage, None, None]:
        """
        Stream parse llms-full.txt, yielding pages one at a time.

        Memory-efficient for large files - only holds one page in memory at a time.

        Args:
            content: Full text content of llms-full.txt file

        Yields:
            DuendePage objects for each documentation page found
        """
        current_title: str | None = None
        current_source: str | None = None
        content_lines: list[str] = []
        in_page = False
        skip_page = False

        for line in content.splitlines():
            # Check for page separator
            if self.SEPARATOR_PATTERN.match(line):
                # Yield previous page if exists and valid
                if current_title and content_lines and not skip_page:
                    page_content = '\n'.join(content_lines).strip()
                    if page_content:  # Only yield non-empty pages
                        category = self._detect_category(current_title, page_content)
                        source_url = current_source or self._derive_url(
                            current_title, category, page_content
                        )
                        doc_id = self._generate_doc_id(current_title, category, source_url)

                        yield DuendePage(
                            title=current_title,
                            content=page_content,
                            source_url=source_url,
                            category=category,
                            doc_id=doc_id,
                        )

                # Reset for next page
                current_title = None
                current_source = None
                content_lines = []
                in_page = False
                skip_page = False
                continue

            # Skip system instructions
            if self.SYSTEM_PATTERN.match(line.strip()):
                continue

            # Check for title (must be first non-empty line after separator)
            if not in_page:
                title_match = self.TITLE_PATTERN.match(line)
                if title_match:
                    current_title = title_match.group(1).strip()
                    # Strip HTML tags (e.g., <br/>) and normalize whitespace
                    current_title = re.sub(r'<[^>]+>', ' ', current_title)
                    current_title = re.sub(r'\s+', ' ', current_title).strip()
                    # Skip certain pages
                    if current_title in ('404 Not Found', '404', 'Not Found'):
                        skip_page = True
                    in_page = True
                    continue
                elif line.strip():
                    # Non-title content before we have a title - skip
                    continue

            # Check for source URL (optional, usually follows title)
            source_match = self.SOURCE_PATTERN.match(line)
            if source_match and current_title and not current_source:
                current_source = source_match.group(1).strip()
                continue

            # Accumulate content
            if in_page:
                content_lines.append(line)

        # Yield final page
        if current_title and content_lines and not skip_page:
            page_content = '\n'.join(content_lines).strip()
            if page_content:
                category = self._detect_category(current_title, page_content)
                source_url = current_source or self._derive_url(
                    current_title, category, page_content
                )
                doc_id = self._generate_doc_id(current_title, category, source_url)

                yield DuendePage(
                    title=current_title,
                    content=page_content,
                    source_url=source_url,
                    category=category,
                    doc_id=doc_id,
                )

    def parse_to_list(self, content: str) -> list[DuendePage]:
        """Parse llms-full.txt and return all pages as a list."""
        return list(self.parse_stream(content))

    def count_pages(self, content: str) -> int:
        """Count pages without storing all content."""
        count = 0
        for _ in self.parse_stream(content):
            count += 1
        return count

    def get_page_by_title(self, content: str, target_title: str) -> DuendePage | None:
        """Find a specific page by title."""
        target_lower = target_title.lower()
        for page in self.parse_stream(content):
            if page.title.lower() == target_lower:
                return page
        return None

    def get_pages_by_category(self, content: str, category: str) -> list[DuendePage]:
        """Get all pages in a specific category."""
        return [
            page for page in self.parse_stream(content)
            if page.category == category
        ]

    def get_categories(self, content: str) -> dict[str | None, int]:
        """Get page counts by category."""
        categories: dict[str | None, int] = {}
        for page in self.parse_stream(content):
            cat = page.category
            categories[cat] = categories.get(cat, 0) + 1
        return categories


def url_to_local_path(source_url: str, base_dir: str | Path, domain_dir: str = 'duendesoftware-com') -> Path:
    """
    Convert a documentation URL to a local file path.

    This helper extracts the path from a URL and combines it with a base directory
    to produce a local file path for storing the documentation.

    Args:
        source_url: Full URL like "https://docs.duendesoftware.com/bff/overview/"
        base_dir: Base output directory (can be string or Path)
        domain_dir: Subdirectory for domain (default: duendesoftware-com)

    Returns:
        Local path like "<base_dir>/duendesoftware-com/bff/overview.md"

    Example:
        >>> url_to_local_path("https://docs.duendesoftware.com/bff/overview/", Path("/canonical"))
        PosixPath('/canonical/duendesoftware-com/bff/overview.md')
    """
    from urllib.parse import urlparse

    if isinstance(base_dir, str):
        base_dir = Path(base_dir)

    parsed = urlparse(source_url)
    path = parsed.path

    # Remove leading/trailing slashes
    path = path.strip('/')

    # Handle empty path
    if not path:
        path = 'index'

    # Ensure .md extension
    if not path.endswith('.md'):
        # Remove trailing slash component if present
        if path.endswith('/'):
            path = path[:-1]
        path = path + '.md'

    return base_dir / domain_dir / path


def parse_llms_full_txt(content: str, base_url: str = 'https://docs.duendesoftware.com') -> Generator[DuendePage, None, None]:
    """
    Convenience function to stream parse Duende's llms-full.txt.

    Args:
        content: llms-full.txt file content
        base_url: Base URL for the documentation

    Yields:
        DuendePage objects
    """
    parser = LlmsFullParser(base_url=base_url)
    yield from parser.parse_stream(content)


if __name__ == '__main__':
    """Self-test for llms_full_parser module."""
    print("llms_full_parser Self-Test (Duende Docs)")
    print("=" * 60)

    # Test with sample content matching Duende's format
    print("\n1. Testing LlmsFullParser with Duende-style format:")
    sample_content = """<SYSTEM>This is the full developer documentation for Duende Software Docs</SYSTEM>
-----
# Duende Software Docs

> Get started building your .NET applications with IdentityServer, Backend-for-Frontend (BFF) and our open-source tools.

Install templates with:
```bash
dotnet new install Duende.Templates
```

[Learn more](/identityserver/)

-----
# 404 Not Found

> Page not found.

-----
# Access Token Management

> The Duende.AccessTokenManagement library provides automatic access token management features for .NET applications

## Machine-To-Machine Token Management

To get started, install the NuGet Package:

```bash
dotnet add package Duende.AccessTokenManagement
```

[Learn more](/accesstokenmanagement/workers/)

-----
# Backend For Frontend (BFF) Security Framework

> A comprehensive security framework for securing browser-based frontends with ASP.NET Core backends

The BFF pattern states that every browser based application should also have a server side application.

[Learn more](/bff/)

-----
# IdentityServer Overview

> The most flexible and standards-compliant OpenID Connect and OAuth 2.0 framework for ASP.NET Core.

IdentityServer is the flagship product from Duende Software.

"""

    parser = LlmsFullParser()
    pages = parser.parse_to_list(sample_content)
    print(f"   Found {len(pages)} pages (404 pages are skipped)")

    for page in pages:
        print(f"\n   Title: {page.title}")
        print(f"   Category: {page.category}")
        print(f"   Doc ID: {page.doc_id}")
        print(f"   URL: {page.source_url}")
        print(f"   Content length: {len(page.content)} chars")

    # Test category counts
    print("\n2. Testing category detection:")
    categories = parser.get_categories(sample_content)
    for cat, count in categories.items():
        print(f"   {cat or 'uncategorized'}: {count} pages")

    # Test URL derivation
    print("\n3. Testing URL to local path conversion:")
    test_urls = [
        "https://docs.duendesoftware.com/bff/overview/",
        "https://docs.duendesoftware.com/identityserver/quickstarts/",
        "https://docs.duendesoftware.com/accesstokenmanagement/workers/",
    ]
    for url in test_urls:
        local_path = url_to_local_path(url, Path("/canonical"))
        print(f"   {url}")
        print(f"   -> {local_path}")

    print("\n" + "=" * 60)
    print("Self-test complete!")
