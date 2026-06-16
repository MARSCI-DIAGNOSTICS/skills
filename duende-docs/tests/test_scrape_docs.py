"""
Tests for scrape_docs.py - Duende documentation scraper.

These tests verify:
1. Frontmatter does NOT include last_fetched (prevents git noise)
2. Index metadata DOES include last_fetched (for tracking)
3. Content hash is correctly included in frontmatter
4. Encoding fixes: double-encoded UTF-8 and smart quote normalization
5. HTML stripping from titles
6. Sitemap URL resolution
"""
import pytest
import yaml


class TestAddFrontmatter:
    """Tests for DuendeDocScraper.add_frontmatter method."""

    def test_frontmatter_excludes_last_fetched(self, mock_duende_page, mock_canonical_dir):
        """Frontmatter should NOT include last_fetched to prevent git noise.

        The last_fetched timestamp is stored ONLY in index.yaml, not in the
        markdown frontmatter. This prevents unnecessary file changes when
        content hasn't changed but timestamp would update.
        """
        from scrape_docs import DuendeDocScraper

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)
        result = scraper.add_frontmatter(mock_duende_page)

        # Parse the frontmatter
        assert result.startswith('---\n')
        frontmatter_end = result.find('---', 3)
        frontmatter_text = result[4:frontmatter_end].strip()
        frontmatter = yaml.safe_load(frontmatter_text)

        # Verify last_fetched is NOT in frontmatter
        assert 'last_fetched' not in frontmatter, (
            "last_fetched should NOT be in markdown frontmatter. "
            "It should only be stored in index.yaml to prevent git noise."
        )

    def test_frontmatter_includes_required_fields(self, mock_duende_page, mock_canonical_dir):
        """Frontmatter should include all required fields except last_fetched."""
        from scrape_docs import DuendeDocScraper

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)
        result = scraper.add_frontmatter(mock_duende_page)

        # Parse the frontmatter
        frontmatter_end = result.find('---', 3)
        frontmatter_text = result[4:frontmatter_end].strip()
        frontmatter = yaml.safe_load(frontmatter_text)

        # Verify required fields ARE present
        assert 'title' in frontmatter
        assert 'source_url' in frontmatter
        assert 'source_type' in frontmatter
        assert 'content_hash' in frontmatter

        # Verify values
        assert frontmatter['title'] == mock_duende_page.title
        assert frontmatter['source_url'] == mock_duende_page.source_url
        assert frontmatter['source_type'] == 'llms-full-txt'
        assert frontmatter['content_hash'].startswith('sha256:')

    def test_frontmatter_includes_optional_fields_when_present(self, mock_canonical_dir):
        """Frontmatter should include category and doc_id when present."""
        from scrape_docs import DuendeDocScraper
        from llms_full_parser import DuendePage

        page = DuendePage(
            title="Test with Category",
            content="Content here",
            source_url="https://docs.duendesoftware.com/test/",
            category="bff",
            doc_id="bff/test-doc"
        )

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)
        result = scraper.add_frontmatter(page)

        # Parse the frontmatter
        frontmatter_end = result.find('---', 3)
        frontmatter_text = result[4:frontmatter_end].strip()
        frontmatter = yaml.safe_load(frontmatter_text)

        # Verify optional fields
        assert frontmatter.get('category') == 'bff'
        assert frontmatter.get('doc_id') == 'bff/test-doc'

    def test_content_hash_is_deterministic(self, mock_duende_page, mock_canonical_dir):
        """Same content should produce same hash (no timestamp contamination)."""
        from scrape_docs import DuendeDocScraper

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)

        # Generate frontmatter twice
        result1 = scraper.add_frontmatter(mock_duende_page)
        result2 = scraper.add_frontmatter(mock_duende_page)

        # Parse both
        def extract_hash(result):
            frontmatter_end = result.find('---', 3)
            frontmatter_text = result[4:frontmatter_end].strip()
            frontmatter = yaml.safe_load(frontmatter_text)
            return frontmatter['content_hash']

        hash1 = extract_hash(result1)
        hash2 = extract_hash(result2)

        # Hashes should be identical
        assert hash1 == hash2, "Content hash should be deterministic"


class TestSavePage:
    """Tests for DuendeDocScraper.save_page method."""

    def test_save_page_returns_metadata_with_last_fetched(self, mock_duende_page, mock_canonical_dir):
        """save_page should return metadata dict that includes last_fetched for index.yaml."""
        from scrape_docs import DuendeDocScraper

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)
        metadata = scraper.save_page(mock_duende_page)

        # Metadata should include last_fetched (for index.yaml)
        assert metadata is not None, "save_page should return metadata dict"
        assert 'last_fetched' in metadata, (
            "Metadata returned by save_page should include last_fetched for index.yaml"
        )
        # last_fetched in index should be date format (YYYY-MM-DD)
        assert len(metadata['last_fetched']) == 10, "last_fetched should be YYYY-MM-DD format"

    def test_saved_file_frontmatter_excludes_last_fetched(self, mock_duende_page, mock_canonical_dir):
        """File written by save_page should NOT have last_fetched in frontmatter."""
        from scrape_docs import DuendeDocScraper

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)
        metadata = scraper.save_page(mock_duende_page)

        # Get the saved file path
        saved_path = mock_canonical_dir / metadata['path']

        # Read and parse the file
        content = saved_path.read_text(encoding='utf-8')
        frontmatter_end = content.find('---', 3)
        frontmatter_text = content[4:frontmatter_end].strip()
        frontmatter = yaml.safe_load(frontmatter_text)

        # File frontmatter should NOT have last_fetched
        assert 'last_fetched' not in frontmatter, (
            "Saved file frontmatter should NOT include last_fetched"
        )


class TestSkipBehavior:
    """Tests for skip behavior when content hasn't changed."""

    def test_skip_when_hash_matches(self, mock_duende_page, mock_canonical_dir):
        """Should skip saving when content hash matches existing file."""
        from scrape_docs import DuendeDocScraper

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)

        # Save once
        metadata1 = scraper.save_page(mock_duende_page)
        assert metadata1 is not None

        # Try to save again - should skip
        metadata2 = scraper.save_page(mock_duende_page)
        assert metadata2 is None, "Should return None when skipping (hash matches)"

        # Stats should show one skip
        assert scraper.stats['skipped_pages'] == 1

    def test_skip_does_not_update_file(self, mock_duende_page, mock_canonical_dir):
        """When skipping, the file should NOT be modified at all."""
        import os
        import time
        from scrape_docs import DuendeDocScraper

        scraper = DuendeDocScraper(base_output_dir=mock_canonical_dir)

        # Save once
        metadata1 = scraper.save_page(mock_duende_page)
        saved_path = mock_canonical_dir / metadata1['path']

        # Get original mtime
        original_mtime = os.path.getmtime(saved_path)

        # Wait a tiny bit to ensure mtime would change if file was touched
        time.sleep(0.01)

        # Try to save again (should skip)
        scraper.save_page(mock_duende_page)

        # mtime should be unchanged
        new_mtime = os.path.getmtime(saved_path)
        assert new_mtime == original_mtime, "File should not be modified when skipping"


class TestEncodingFix:
    """Tests for DuendeDocScraper._fix_encoding method."""

    def test_smart_double_quotes_normalized(self):
        """Left/right double quotes should become ASCII double quotes."""
        from scrape_docs import DuendeDocScraper

        result = DuendeDocScraper._fix_encoding('\u201cinactivity timeout\u201d')
        assert result == '"inactivity timeout"'

    def test_smart_single_quotes_normalized(self):
        """Left/right single quotes should become ASCII apostrophes."""
        from scrape_docs import DuendeDocScraper

        result = DuendeDocScraper._fix_encoding('user\u2019s token')
        assert result == "user's token"

    def test_en_dash_normalized(self):
        """En dash should become ASCII hyphen."""
        from scrape_docs import DuendeDocScraper

        result = DuendeDocScraper._fix_encoding('pages 1\u20135')
        assert result == 'pages 1-5'

    def test_em_dash_normalized(self):
        """Em dash should become double hyphen."""
        from scrape_docs import DuendeDocScraper

        result = DuendeDocScraper._fix_encoding('token\u2014expired')
        assert result == 'token--expired'

    def test_ellipsis_normalized(self):
        """Ellipsis should become three dots."""
        from scrape_docs import DuendeDocScraper

        result = DuendeDocScraper._fix_encoding('loading\u2026')
        assert result == 'loading...'

    def test_plain_ascii_passthrough(self):
        """Plain ASCII content should pass through unchanged."""
        from scrape_docs import DuendeDocScraper

        content = 'This is plain ASCII text with "quotes" and dashes-here.'
        result = DuendeDocScraper._fix_encoding(content)
        assert result == content

    def test_double_encoding_reversal(self):
        """Double-encoded UTF-8 should be reversed then normalized.

        When UTF-8 smart quotes are double-encoded, the 3-byte UTF-8 sequence
        for e.g. a left double quote (\u201c = 0xE2 0x80 0x9C) gets interpreted
        as Latin-1, producing garbled characters. This test simulates that.
        """
        from scrape_docs import DuendeDocScraper

        # Simulate double-encoding: encode UTF-8 smart quotes, then decode as Latin-1
        original = '\u201cinactivity timeout\u201d'
        double_encoded = original.encode('utf-8').decode('latin-1')

        result = DuendeDocScraper._fix_encoding(double_encoded)
        assert result == '"inactivity timeout"'


class TestHtmlTitleStripping:
    """Tests for HTML tag stripping from titles in parse_stream."""

    def test_br_tag_removed_from_title(self):
        """<br/> tags in title should be replaced with space."""
        from llms_full_parser import LlmsFullParser

        content = "-----\n# Duende Software<br/> Docs\n\nContent here.\n-----"
        parser = LlmsFullParser()
        pages = list(parser.parse_stream(content))

        assert len(pages) == 1
        assert pages[0].title == 'Duende Software Docs'

    def test_clean_title_passthrough(self):
        """Titles without HTML should pass through unchanged."""
        from llms_full_parser import LlmsFullParser

        content = "-----\n# Access Token Management\n\nContent here.\n-----"
        parser = LlmsFullParser()
        pages = list(parser.parse_stream(content))

        assert len(pages) == 1
        assert pages[0].title == 'Access Token Management'

    def test_multiple_html_tags_stripped(self):
        """Multiple HTML tags should all be stripped."""
        from llms_full_parser import LlmsFullParser

        content = "-----\n# Title <b>Bold</b> and <i>Italic</i>\n\nContent.\n-----"
        parser = LlmsFullParser()
        pages = list(parser.parse_stream(content))

        assert len(pages) == 1
        assert pages[0].title == 'Title Bold and Italic'


class TestSitemapUrlResolver:
    """Tests for SitemapUrlResolver class."""

    def test_single_slug_resolution(self):
        """Should resolve a unique slug to its full URL."""
        from llms_full_parser import SitemapUrlResolver

        resolver = SitemapUrlResolver()
        resolver.load_from_urls([
            'https://docs.duendesoftware.com/identityserver/ui/server-side-sessions/inactivity-timeout/',
            'https://docs.duendesoftware.com/bff/overview/',
        ])

        result = resolver.resolve('inactivity-timeout')
        assert result == 'https://docs.duendesoftware.com/identityserver/ui/server-side-sessions/inactivity-timeout/'

    def test_category_disambiguation(self):
        """Should use category to disambiguate when slug appears in multiple paths."""
        from llms_full_parser import SitemapUrlResolver

        resolver = SitemapUrlResolver()
        resolver.load_from_urls([
            'https://docs.duendesoftware.com/general/logging/',
            'https://docs.duendesoftware.com/identityserver/diagnostics/logging/',
            'https://docs.duendesoftware.com/accesstokenmanagement/advanced/logging/',
        ])

        # With category, should disambiguate
        result = resolver.resolve('logging', category='identityserver')
        assert result == 'https://docs.duendesoftware.com/identityserver/diagnostics/logging/'

        result = resolver.resolve('logging', category='general')
        assert result == 'https://docs.duendesoftware.com/general/logging/'

    def test_unknown_slug_returns_none(self):
        """Should return None for slugs not found in sitemap."""
        from llms_full_parser import SitemapUrlResolver

        resolver = SitemapUrlResolver()
        resolver.load_from_urls([
            'https://docs.duendesoftware.com/bff/overview/',
        ])

        result = resolver.resolve('nonexistent-page')
        assert result is None

    def test_parser_integration_with_resolver(self):
        """Parser should use resolver when available."""
        from llms_full_parser import LlmsFullParser, SitemapUrlResolver

        resolver = SitemapUrlResolver()
        resolver.load_from_urls([
            'https://docs.duendesoftware.com/identityserver/ui/server-side-sessions/inactivity-timeout/',
        ])

        parser = LlmsFullParser(url_resolver=resolver)
        content = "-----\n# Inactivity Timeout\n\nSome content about timeouts.\n-----"
        pages = list(parser.parse_stream(content))

        assert len(pages) == 1
        assert pages[0].source_url == 'https://docs.duendesoftware.com/identityserver/ui/server-side-sessions/inactivity-timeout/'

    def test_resolver_fallback_when_no_match(self):
        """Parser should fall back to title-based URL when resolver has no match."""
        from llms_full_parser import LlmsFullParser, SitemapUrlResolver

        resolver = SitemapUrlResolver()
        resolver.load_from_urls([
            'https://docs.duendesoftware.com/bff/overview/',
        ])

        parser = LlmsFullParser(url_resolver=resolver)
        content = "-----\n# Some Unknown Page\n\nContent here.\n-----"
        pages = list(parser.parse_stream(content))

        assert len(pages) == 1
        # Should fall back to title-based URL derivation
        assert 'some-unknown-page' in pages[0].source_url
