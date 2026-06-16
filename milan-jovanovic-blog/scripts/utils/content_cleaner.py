#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
content_cleaner.py - Content cleanup for Milan Jovanovic blog articles.

Removes promotional content while preserving educational material:
- Sponsor sections (between title and first H2)
- Promotional footer ("Whenever you're ready, there are X ways...")
- Newsletter signup sections
- Course CTAs and sidebar
- Reading time metadata
- "Manage read history" links
"""

import re
from dataclasses import dataclass, field
from typing import List


@dataclass
class CleaningResult:
    """Result of content cleaning operation."""
    content: str
    sections_removed: int = 0
    inline_removals: int = 0
    stop_triggered: bool = False
    removed_sections: List[dict] = field(default_factory=list)


class MilanContentCleaner:
    """
    Content cleaner specialized for Milan Jovanovic blog articles.

    Handles:
    1. Sponsor section detection and removal (variable content)
    2. Promotional footer removal
    3. Inline cleanup (reading time, empty images)
    4. Preserves all educational content and code blocks
    """

    # Promotional footer patterns (stop processing after these)
    FOOTER_PATTERNS = [
        re.compile(r"^[-*]{3,}\s*$\n+Whenever you're ready", re.MULTILINE),
        re.compile(r"^Whenever you're ready,\s+there are \d+ ways I can help you", re.MULTILINE),
        re.compile(r"^Become a Better \.NET Software Engineer", re.MULTILINE),
        re.compile(r"^Accelerate Your \.NET Skills", re.MULTILINE),
        re.compile(r"^## Hi, I'm Milan", re.MULTILINE),
    ]

    # Sponsor detection patterns
    SPONSOR_PATTERNS = [
        re.compile(r'Get a .*?speedy and scalable.*?enterprise', re.IGNORECASE | re.DOTALL),
        re.compile(r'AuthKit.*?WorkOS', re.IGNORECASE | re.DOTALL),
        re.compile(r'\[Sponsor this newsletter\]', re.IGNORECASE),
        re.compile(r'Incident responders.*?catch up', re.IGNORECASE | re.DOTALL),
        re.compile(r'SEV0.*?on-demand', re.IGNORECASE | re.DOTALL),
    ]

    # Inline patterns to remove
    READING_TIME_PATTERN = re.compile(r'\d+\s*min\s*read\s*[·•\-]?\s*', re.IGNORECASE)
    EMPTY_IMAGE_PATTERN = re.compile(r'^\!\[\]\(<Base64-Image-Removed>\)\s*$', re.MULTILINE)
    MANAGE_HISTORY_PATTERN = re.compile(r'\[Manage read history\]\([^\)]+\)')
    DATE_DOTS_PATTERN = re.compile(r'([·•])\s*\1')  # Remove duplicate dots

    def clean_content(self, content: str, url: str | None = None) -> CleaningResult:
        """
        Clean article content by removing promotional sections.

        Args:
            content: Raw markdown content from scrape
            url: Article URL (for logging)

        Returns:
            CleaningResult with cleaned content and statistics
        """
        result = CleaningResult(content=content)

        # Step 1: Stop at promotional footer first (removes most promo content)
        content = self._stop_at_footer(content, result)

        # Step 2: Remove sponsor section (between title and first H2)
        content = self._remove_sponsor_section(content, result)

        # Step 3: Clean inline patterns
        content = self._clean_inline(content, result)

        # Step 4: Normalize whitespace
        content = self._normalize_whitespace(content)

        result.content = content.strip()
        return result

    def _stop_at_footer(self, content: str, result: CleaningResult) -> str:
        """Stop processing at promotional footer."""
        earliest_match = None
        earliest_pos = len(content)

        for pattern in self.FOOTER_PATTERNS:
            match = pattern.search(content)
            if match and match.start() < earliest_pos:
                earliest_match = match
                earliest_pos = match.start()

        if earliest_match:
            result.stop_triggered = True
            result.sections_removed += 1
            result.removed_sections.append({
                'type': 'footer',
                'position': earliest_pos
            })
            # Also remove trailing separator line if present
            cleaned = content[:earliest_pos].rstrip()
            # Remove trailing separator (---, ***, etc.)
            cleaned = re.sub(r'\n\s*[-*]{3,}\s*$', '', cleaned)
            return cleaned

        return content

    def _remove_sponsor_section(self, content: str, result: CleaningResult) -> str:
        """
        Remove sponsor section between header and first H2.
        """
        lines = content.split('\n')

        # Find H1 and first H2
        h1_idx = None
        first_h2_idx = None

        for i, line in enumerate(lines):
            if line.startswith('# ') and h1_idx is None:
                h1_idx = i
            elif line.startswith('## ') and first_h2_idx is None:
                first_h2_idx = i
                break

        if h1_idx is None or first_h2_idx is None:
            return content

        # Get the header section
        header_section = '\n'.join(lines[h1_idx+1:first_h2_idx])

        # Check for sponsor content
        has_sponsor = any(p.search(header_section) for p in self.SPONSOR_PATTERNS)

        if has_sponsor:
            # Keep only title and date line
            preserved = [lines[h1_idx]]

            # Look for date line in first few lines after H1
            for line in lines[h1_idx+1:min(h1_idx+5, first_h2_idx)]:
                if self._is_date_line(line):
                    preserved.append(line)
                    break

            # Reconstruct without sponsor content
            clean_lines = preserved + [''] + lines[first_h2_idx:]

            result.sections_removed += 1
            result.removed_sections.append({
                'type': 'sponsor',
                'line_start': h1_idx + 1,
                'line_end': first_h2_idx
            })

            return '\n'.join(clean_lines)

        return content

    def _is_date_line(self, line: str) -> bool:
        """Check if line contains article date."""
        date_patterns = [
            r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            r'\b\d{4}-\d{2}-\d{2}\b',
        ]
        return any(re.search(p, line) for p in date_patterns)

    def _clean_inline(self, content: str, result: CleaningResult) -> str:
        """Remove inline patterns."""
        # Remove empty image placeholders
        content, count = self.EMPTY_IMAGE_PATTERN.subn('', content)
        result.inline_removals += count

        # Remove manage history links
        content, count = self.MANAGE_HISTORY_PATTERN.subn('', content)
        result.inline_removals += count

        # Remove reading time (but keep date)
        content, count = self.READING_TIME_PATTERN.subn('', content)
        result.inline_removals += count

        # Clean up duplicate dots/bullets
        content, count = self.DATE_DOTS_PATTERN.subn(r'\1', content)
        result.inline_removals += count

        return content

    def _normalize_whitespace(self, content: str) -> str:
        """Normalize whitespace in content."""
        # Remove multiple consecutive blank lines
        content = re.sub(r'\n{3,}', '\n\n', content)

        # Remove trailing whitespace from lines
        lines = [line.rstrip() for line in content.split('\n')]

        return '\n'.join(lines)


def clean_article(content: str, url: str | None = None) -> str:
    """
    Convenience function to clean article content.

    Args:
        content: Raw markdown content
        url: Optional URL for logging

    Returns:
        Cleaned markdown content
    """
    cleaner = MilanContentCleaner()
    result = cleaner.clean_content(content, url)
    return result.content


if __name__ == '__main__':
    # Test with sample content
    sample = """
# Test Article Title

5 min read·December 20, 2025··

[Manage read history](https://example.com)

Get a **speedy and scalable enterprise ready login box** from AuthKit.
[Sponsor this newsletter](https://example.com)

## First Section

This is the actual content.

```python
def hello():
    print("Hello, World!")
```

## Second Section

More educational content here.

---

Whenever you're ready, there are 4 ways I can help you:

1. Course 1
2. Course 2

Become a Better .NET Software Engineer
Join 75,000+ engineers...
"""

    result = clean_article(sample)
    print("=== Cleaned Content ===")
    print(result)
