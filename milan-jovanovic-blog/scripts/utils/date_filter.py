#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
date_filter.py - Date filtering for Milan Jovanovic blog articles.

Supports:
- 6-month rolling window (default)
- Fixed date cutoff (DOTNET_10_RELEASE for legacy compatibility)
"""

from datetime import datetime, timezone, timedelta
from typing import Optional

# .NET 10 GA release date - for legacy compatibility
DOTNET_10_RELEASE = datetime(2025, 11, 1, tzinfo=timezone.utc)

# Rolling window configuration (in months)
ROLLING_WINDOW_MONTHS = 6


def get_rolling_cutoff(months: int = ROLLING_WINDOW_MONTHS) -> datetime:
    """Get cutoff date as N months ago from today."""
    now = datetime.now(timezone.utc)
    # Approximate months as 30 days
    cutoff = now - timedelta(days=months * 30)
    return cutoff.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

# Date parsing formats
DATE_FORMATS = [
    "%Y-%m-%dT%H:%M:%S.%fZ",      # ISO 8601 with milliseconds
    "%Y-%m-%dT%H:%M:%SZ",          # ISO 8601 without milliseconds
    "%Y-%m-%dT%H:%M:%S%z",         # ISO 8601 with timezone
    "%Y-%m-%dT%H:%M:%S.%f%z",      # ISO 8601 with milliseconds and timezone
    "%Y-%m-%d",                     # Date only
    "%B %d, %Y",                    # "November 15, 2025"
    "%b %d, %Y",                    # "Nov 15, 2025"
]


def parse_date(date_str: str) -> Optional[datetime]:
    """
    Parse date string to UTC datetime.

    Args:
        date_str: Date string in various formats

    Returns:
        datetime in UTC, or None if parsing fails
    """
    if not date_str:
        return None

    # Handle 'Z' suffix (UTC)
    date_str = date_str.replace('Z', '+00:00') if date_str.endswith('Z') else date_str

    for fmt in DATE_FORMATS:
        try:
            dt = datetime.strptime(date_str.replace('+00:00', 'Z').replace('Z', ''),
                                   fmt.replace('Z', '').replace('%z', ''))
            if dt.tzinfo is None:
                dt = dt.replace(tzinfo=timezone.utc)
            return dt
        except ValueError:
            continue

    # Try ISO format parsing (Python 3.7+)
    try:
        # Handle timezone suffix
        if '+' in date_str or date_str.endswith('Z'):
            clean = date_str.replace('Z', '+00:00')
            dt = datetime.fromisoformat(clean)
        else:
            dt = datetime.fromisoformat(date_str)

        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except ValueError:
        pass

    return None


def is_after_cutoff(
    date: datetime | str | None,
    cutoff: datetime = DOTNET_10_RELEASE
) -> bool:
    """
    Check if date is on or after the cutoff date.

    Args:
        date: datetime, date string, or None
        cutoff: Minimum date threshold (defaults to DOTNET_10_RELEASE)

    Returns:
        True if article should be included
    """
    if date is None:
        return False

    if isinstance(date, str):
        date = parse_date(date)
        if date is None:
            return False

    # Ensure both have timezone info
    if date.tzinfo is None:
        date = date.replace(tzinfo=timezone.utc)
    if cutoff.tzinfo is None:
        cutoff = cutoff.replace(tzinfo=timezone.utc)

    return date >= cutoff


def should_include_article(
    published_at: str | datetime | None,
    min_date: str | datetime | None = None
) -> bool:
    """
    Determine if article should be included based on publication date.

    Args:
        published_at: Article publication date
        min_date: Minimum date threshold (defaults to DOTNET_10_RELEASE)

    Returns:
        True if article should be included
    """
    if min_date is None:
        cutoff = DOTNET_10_RELEASE
    elif isinstance(min_date, str):
        cutoff = parse_date(min_date)
        if cutoff is None:
            cutoff = DOTNET_10_RELEASE
    else:
        cutoff = min_date

    return is_after_cutoff(published_at, cutoff)


def extract_date_from_metadata(metadata: dict) -> Optional[datetime]:
    """
    Extract publication date from scrape metadata.

    Tries multiple metadata fields in priority order.

    Args:
        metadata: Firecrawl scrape metadata dict

    Returns:
        datetime in UTC, or None if not found
    """
    # Priority order of metadata fields
    date_fields = [
        'article:published_time',
        'publishedTime',
        'publish_date',
        'datePublished',
        'og:published_time',
    ]

    for field in date_fields:
        value = metadata.get(field)
        if value:
            parsed = parse_date(value)
            if parsed:
                return parsed

    return None


def get_cutoff_date(
    since: str | None = None,
    use_rolling: bool = True,
    months: int = ROLLING_WINDOW_MONTHS,
) -> datetime:
    """
    Get the cutoff date for filtering.

    Args:
        since: Optional date string override (YYYY-MM-DD)
        use_rolling: If True, use rolling window (default). If False, use DOTNET_10_RELEASE.
        months: Number of months for rolling window (default: 6)

    Returns:
        Cutoff datetime in UTC
    """
    if since:
        parsed = parse_date(since)
        if parsed:
            return parsed

    if use_rolling:
        return get_rolling_cutoff(months)

    return DOTNET_10_RELEASE


if __name__ == '__main__':
    # Test date parsing and filtering
    test_dates = [
        "2025-11-15T00:00:00.000Z",
        "2025-12-20T00:00:00.000Z",
        "2025-10-15T00:00:00.000Z",  # Before cutoff
        "November 15, 2025",
        "2024-06-01",  # Way before cutoff
    ]

    print(f"Cutoff date: {DOTNET_10_RELEASE.date()}")
    print()

    for date_str in test_dates:
        parsed = parse_date(date_str)
        included = should_include_article(date_str)
        status = "INCLUDE" if included else "EXCLUDE"
        print(f"{date_str:40} -> {parsed.date() if parsed else 'PARSE ERROR':12} [{status}]")
