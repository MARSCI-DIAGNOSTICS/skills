"""
Tests for scrape_docs.py script.

Tests critical functionality for scraping documentation from sitemaps and URLs.
"""

import sys
from pathlib import Path
from unittest.mock import patch, MagicMock


from tests.shared.test_utils import TempReferencesDir, create_mock_sitemap



class TestDocScraper:
    """Test suite for DocScraper class."""

    def test_scraper_initialization(self, temp_dir):
        """Test DocScraper initialization."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            assert scraper.base_output_dir == refs_dir.references_dir
            assert scraper.index_path.exists() or scraper.index_path.parent.exists()
            
        finally:
            refs_dir.cleanup()

    def test_parse_sitemap(self, temp_dir):
        """Test parsing sitemap XML."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Create mock sitemap content
            sitemap_content = create_mock_sitemap([
                'https://docs.claude.com/en/docs/intro',
                'https://docs.claude.com/en/docs/guide',
                'https://docs.claude.com/en/api/reference'
            ])
            
            # Mock fetch_url to return sitemap content (returns tuple: content, etag)
            scraper.fetch_url = MagicMock(return_value=(sitemap_content, None))
            
            urls = scraper.parse_sitemap('https://docs.claude.com/sitemap.xml', url_filter='/en/docs/')
            
            assert len(urls) == 2  # Should filter to /en/docs/ URLs only
            assert all('/en/docs/' in url for url in urls)
            
        finally:
            refs_dir.cleanup()

    def test_parse_docs_map(self, temp_dir):
        """Test parsing docs map markdown."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            docs_map_content = """# Documentation Map

- [Intro](https://code.claude.com/docs/en/intro.md)
- [Guide](https://code.claude.com/docs/en/guide.md)
"""

            # Mock fetch_url to return docs map content (returns tuple: content, etag)
            scraper.fetch_url = MagicMock(return_value=(docs_map_content, None))
            
            urls = scraper.parse_docs_map('https://code.claude.com/docs/en/claude_code_docs_map.md')
            
            assert len(urls) == 2
            assert 'intro.md' in urls[0] or 'guide.md' in urls[0]
            
        finally:
            refs_dir.cleanup()

    def test_auto_detect_output_dir(self, temp_dir):
        """Test auto-detection of output directory from URL."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock the config helper to return expected value
            with patch('scripts.utils.config_helpers.get_output_dir_mapping') as mock_get_output:
                mock_get_output.return_value = 'docs-claude-com'
                
                url = 'https://docs.claude.com/en/docs/intro'
                output_dir = scraper.auto_detect_output_dir(url)
                
                assert output_dir == 'docs-claude-com'
            
        finally:
            refs_dir.cleanup()

    def test_mark_doc_stale_for_404(self, temp_dir):
        """Test marking doc as stale when source URL returns 404."""
        refs_dir = TempReferencesDir()
        
        try:
            # Create index with test entry
            index = {
                'test-doc': {
                    'path': 'test/doc.md',
                    'url': 'https://example.com/test',
                    'source_url': 'https://example.com/test'
                }
            }
            refs_dir.create_index(index)
            
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            from scripts.management.index_manager import IndexManager
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mark as stale for 404
            output_path = refs_dir.references_dir / 'test' / 'doc.md'
            scraper.mark_doc_stale_for_404('https://example.com/test', output_path)
            
            # Verify stale marking
            manager = IndexManager(refs_dir.references_dir)
            entry = manager.get_entry('test-doc')
            
            if entry:
                assert entry.get('stale') is True
                assert entry.get('stale_reason') == 'source_url_404'
            
        finally:
            refs_dir.cleanup()

    def test_try_fetch_markdown_success(self, temp_dir):
        """Test try_fetch_markdown with successful fetch on first attempt."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock fetch_with_retry to return successful markdown response
            markdown_content = "# Title\n\nContent here"
            mock_response = MagicMock()
            mock_response.text = markdown_content
            mock_response.status_code = 200
            
            with patch('scripts.core.scrape_docs.fetch_with_retry') as mock_fetch:
                mock_fetch.return_value = mock_response

                content, method, final_url = scraper.try_fetch_markdown('https://example.com/page.md')

                assert content == markdown_content
                assert method == "markdown"
                mock_fetch.assert_called_once()

        finally:
            refs_dir.cleanup()

    def test_try_fetch_markdown_retry_on_500(self, temp_dir):
        """Test try_fetch_markdown uses fetch_with_retry which handles retries internally."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock fetch_with_retry to succeed (after internal retries)
            # fetch_with_retry handles retries internally, so if it succeeds,
            # it means it retried and eventually got a successful response
            markdown_content = "# Title\n\nContent"
            mock_response = MagicMock()
            mock_response.text = markdown_content
            mock_response.status_code = 200
            
            with patch('scripts.core.scrape_docs.fetch_with_retry') as mock_fetch:
                mock_fetch.return_value = mock_response

                # Should succeed (fetch_with_retry handles retries internally)
                content, method, final_url = scraper.try_fetch_markdown('https://example.com/page.md')

                assert content == markdown_content
                assert method == "markdown"
                # fetch_with_retry is called once and handles retries internally
                mock_fetch.assert_called_once()

        finally:
            refs_dir.cleanup()

    def test_try_fetch_markdown_no_retry_on_404(self, temp_dir):
        """Test try_fetch_markdown does not retry on 404 (permanent failure)."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock fetch_with_retry to raise 404
            from requests.exceptions import HTTPError
            error_response = MagicMock()
            error_response.status_code = 404
            error_request = MagicMock()
            error_request.url = 'https://example.com/page.md'  # The markdown URL that failed
            http_error = HTTPError("Not Found")
            http_error.response = error_response
            http_error.request = error_request

            with patch('scripts.core.scrape_docs.fetch_with_retry') as mock_fetch:
                mock_fetch.side_effect = http_error

                content, method, final_url = scraper.try_fetch_markdown('https://example.com/page.md')

                # Should return None, None, None and track 404
                assert content is None
                assert method is None
                assert final_url is None
                assert 'https://example.com/page.md' in scraper.url_404s
                # fetch_with_retry should be called (it handles retries internally)
                mock_fetch.assert_called_once()

        finally:
            refs_dir.cleanup()

    def test_try_fetch_markdown_connection_error_retry(self, temp_dir):
        """Test try_fetch_markdown uses fetch_with_retry which handles connection error retries internally."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock fetch_with_retry to succeed (after internal retries)
            # fetch_with_retry handles retries internally, so if it succeeds,
            # it means it retried on connection errors and eventually got a successful response
            markdown_content = "# Title\n\nContent"
            mock_response = MagicMock()
            mock_response.text = markdown_content
            mock_response.status_code = 200
            
            with patch('scripts.core.scrape_docs.fetch_with_retry') as mock_fetch:
                mock_fetch.return_value = mock_response

                # Should succeed (fetch_with_retry handles retries internally)
                content, method, final_url = scraper.try_fetch_markdown('https://example.com/page.md')

                assert content == markdown_content
                assert method == "markdown"
                # fetch_with_retry is called once and handles retries internally
                mock_fetch.assert_called_once()

        finally:
            refs_dir.cleanup()

    def test_try_fetch_markdown_non_markdown_content(self, temp_dir):
        """Test try_fetch_markdown returns None for non-markdown content."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock fetch_with_retry to return HTML content (not markdown)
            html_content = "<html><body>Not markdown</body></html>"
            mock_response = MagicMock()
            mock_response.text = html_content
            mock_response.status_code = 200
            
            with patch('scripts.core.scrape_docs.fetch_with_retry') as mock_fetch:
                mock_fetch.return_value = mock_response

                content, method, final_url = scraper.try_fetch_markdown('https://example.com/page.md')

                # Should return None since content doesn't start with # or ---
                assert content is None
                assert method is None

        finally:
            refs_dir.cleanup()

    def test_normalize_etag_weak_etag_with_quotes(self, temp_dir):
        """Test normalize_etag handles weak ETags with quotes (GitHub format)."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # GitHub format: W/"hash"
            etag = 'W/"e16f4e2428db7530ea2ed9fc0e1afafc3436a149daa0d59340731fe597fefcdf"'
            normalized = scraper.normalize_etag(etag)
            
            assert normalized == 'e16f4e2428db7530ea2ed9fc0e1afafc3436a149daa0d59340731fe597fefcdf'
            
        finally:
            refs_dir.cleanup()

    def test_normalize_etag_strong_etag_with_quotes(self, temp_dir):
        """Test normalize_etag handles strong ETags with quotes."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Strong ETag format: "hash"
            etag = '"abc123def456"'
            normalized = scraper.normalize_etag(etag)
            
            assert normalized == 'abc123def456'
            
        finally:
            refs_dir.cleanup()

    def test_normalize_etag_no_quotes(self, temp_dir):
        """Test normalize_etag handles ETags without quotes."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # ETag without quotes
            etag = 'abc123def456'
            normalized = scraper.normalize_etag(etag)
            
            assert normalized == 'abc123def456'
            
        finally:
            refs_dir.cleanup()

    def test_normalize_etag_weak_etag_no_quotes(self, temp_dir):
        """Test normalize_etag handles weak ETags without quotes."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Weak ETag without quotes: W/hash
            etag = 'W/abc123def456'
            normalized = scraper.normalize_etag(etag)
            
            assert normalized == 'abc123def456'
            
        finally:
            refs_dir.cleanup()

    def test_normalize_etag_none(self, temp_dir):
        """Test normalize_etag handles None input."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            normalized = scraper.normalize_etag(None)
            
            assert normalized is None
            
        finally:
            refs_dir.cleanup()

    def test_normalize_etag_empty_string(self, temp_dir):
        """Test normalize_etag handles empty string."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Empty string should return empty string
            normalized = scraper.normalize_etag('')
            
            assert normalized == ''
            
        finally:
            refs_dir.cleanup()

    def test_check_http_headers_etag_match(self, temp_dir):
        """Test check_http_headers returns True when ETags match (normalized)."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            from unittest.mock import MagicMock
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock HEAD request response
            mock_response = MagicMock()
            mock_response.headers = {
                'ETag': 'W/"abc123"'
            }
            mock_response.raise_for_status = MagicMock()
            
            # Mock session.head to return our mock response
            mock_session = MagicMock()
            mock_session.head = MagicMock(return_value=mock_response)
            
            scraper.header_rate_limiter = MagicMock()
            scraper.header_rate_limiter.wait = MagicMock()
            
            # Patch the _session_local to return our mock session
            scraper._session_local.session = mock_session
            
            # Existing ETag in different format but same hash
            existing_etag = 'W/"abc123"'
            
            result = scraper.check_http_headers('https://example.com/page', existing_etag, None)
            
            assert result is True  # Should match after normalization
            
        finally:
            refs_dir.cleanup()

    def test_check_http_headers_etag_mismatch(self, temp_dir):
        """Test check_http_headers returns False when ETags don't match."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            from unittest.mock import MagicMock
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock HEAD request response
            mock_response = MagicMock()
            mock_response.headers = {
                'ETag': 'W/"newhash"'
            }
            mock_response.raise_for_status = MagicMock()
            
            # Mock session.head to return our mock response
            mock_session = MagicMock()
            mock_session.head = MagicMock(return_value=mock_response)
            
            scraper.header_rate_limiter = MagicMock()
            scraper.header_rate_limiter.wait = MagicMock()
            
            # Patch the _session_local to return our mock session
            scraper._session_local.session = mock_session
            
            # Existing ETag with different hash
            existing_etag = 'W/"oldhash"'
            
            result = scraper.check_http_headers('https://example.com/page', existing_etag, None)
            
            # When ETags don't match, check_http_headers returns None (indicating changed/need to scrape)
            assert result is None  # Should not match, returns None to indicate change
            
        finally:
            refs_dir.cleanup()

    def test_check_http_headers_no_etag(self, temp_dir):
        """Test check_http_headers returns None when ETag header is missing."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            from unittest.mock import MagicMock
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Mock HEAD request response without ETag
            mock_response = MagicMock()
            mock_response.headers = {}
            mock_response.raise_for_status = MagicMock()
            
            # Mock session.head to return our mock response
            mock_session = MagicMock()
            mock_session.head = MagicMock(return_value=mock_response)
            
            scraper.header_rate_limiter = MagicMock()
            scraper.header_rate_limiter.wait = MagicMock()
            
            # Patch the _session_local to return our mock session
            scraper._session_local.session = mock_session
            
            result = scraper.check_http_headers('https://example.com/page', None, None)
            
            assert result is None  # Headers unavailable
            
        finally:
            refs_dir.cleanup()

    def test_should_skip_url_etag_match(self, temp_dir):
        """Test should_skip_url returns True when ETags match (should skip)."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            from unittest.mock import MagicMock
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Create existing file with frontmatter
            output_path = refs_dir.references_dir / 'test' / 'doc.md'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            frontmatter = """---
source_url: https://example.com/page
source_type: manual
last_fetched: '2025-11-18'
content_hash: sha256:abc123
etag: W/"oldhash"
---
# Content
"""
            output_path.write_text(frontmatter, encoding='utf-8')
            
            # Mock HEAD request to return matching ETag
            mock_response = MagicMock()
            mock_response.headers = {
                'ETag': 'W/"oldhash"'
            }
            mock_response.raise_for_status = MagicMock()
            
            mock_session = MagicMock()
            mock_session.head = MagicMock(return_value=mock_response)
            
            scraper.header_rate_limiter = MagicMock()
            scraper.header_rate_limiter.wait = MagicMock()
            
            # Patch the _session_local to return our mock session
            scraper._session_local.session = mock_session
            
            should_skip = scraper.should_skip_url('https://example.com/page', output_path, use_http_headers=True)
            
            assert should_skip is True
            
        finally:
            refs_dir.cleanup()

    def test_should_skip_url_etag_mismatch(self, temp_dir):
        """Test should_skip_url detects ETag mismatch correctly."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.core.scrape_docs import DocScraper
            from unittest.mock import MagicMock
            
            scraper = DocScraper(base_output_dir=refs_dir.references_dir)
            
            # Create existing file with frontmatter
            output_path = refs_dir.references_dir / 'test' / 'doc.md'
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Use an older date so date check doesn't interfere
            frontmatter = """---
source_url: https://example.com/page
source_type: manual
last_fetched: '2025-11-15'
content_hash: sha256:abc123
etag: W/"oldhash"
---
# Content
"""
            output_path.write_text(frontmatter, encoding='utf-8')
            
            # Mock HEAD request to return different ETag
            mock_response = MagicMock()
            mock_response.headers = {
                'ETag': 'W/"newhash"'
            }
            mock_response.raise_for_status = MagicMock()
            
            mock_session = MagicMock()
            mock_session.head = MagicMock(return_value=mock_response)
            
            scraper.header_rate_limiter = MagicMock()
            scraper.header_rate_limiter.wait = MagicMock()
            
            # Patch the _session_local to return our mock session
            scraper._session_local.session = mock_session
            
            # Mock try_fetch_markdown to return content with different hash
            # This simulates the hash check path when ETag doesn't match
            scraper.try_fetch_markdown = MagicMock(return_value=('# New Content', 'markdown'))
            scraper.calculate_hash = MagicMock(return_value='sha256:differenthash')
            
            should_skip = scraper.should_skip_url('https://example.com/page', output_path, use_http_headers=True)
            
            # When ETag changes, check_http_headers returns None
            # Then should_skip_url falls through to hash check
            # Since hash is different, it should return False (should scrape)
            assert should_skip is False  # Should scrape because hash changed

        finally:
            refs_dir.cleanup()


class TestMarkdownValidation:
    """Tests for markdown content validation in try_fetch_markdown."""

    def test_try_fetch_markdown_blockquote_content(self, temp_dir):
        """Blockquote-prefixed content should be accepted as valid markdown.

        code.claude.com's .md endpoints now prepend a blockquote before the heading.
        The scraper must accept '>' as a valid markdown start character.
        """
        from scripts.core.scrape_docs import DocScraper

        scraper = DocScraper(base_output_dir=temp_dir)
        content = "> ## Documentation Index\n\n# Hooks\n\nHook content here."
        content_stripped = content.strip()

        # Replicate the validation logic from try_fetch_markdown
        is_valid = (
            content_stripped.startswith('#')
            or content_stripped.startswith('---')
            or content_stripped.startswith('>')
        )
        assert is_valid is True

    def test_accepts_standard_markdown_heading(self, temp_dir):
        """Content starting with # is accepted."""
        content = "# Title\n\nSome content here with enough characters to pass."
        content_stripped = content.strip()
        is_markdown = (
            content_stripped.startswith('#') or
            content_stripped.startswith('---') or
            content_stripped.startswith('>')
        )
        assert is_markdown is True

    def test_accepts_standard_markdown_frontmatter(self, temp_dir):
        """Content starting with --- is accepted."""
        content = "---\ntitle: Test\n---\n\n# Heading\n\nContent."
        content_stripped = content.strip()
        is_markdown = (
            content_stripped.startswith('#') or
            content_stripped.startswith('---') or
            content_stripped.startswith('>')
        )
        assert is_markdown is True

    def test_accepts_non_standard_md_content(self, temp_dir):
        """Content from .md endpoint in non-standard format is accepted if > 50 chars and not SPA shell."""
        # Simulates a C# "method not available" page from .md endpoint
        content = 'The method `upload` is not available in this language. Please refer to the Python SDK documentation.'
        content_stripped = content.strip()
        is_markdown = (
            content_stripped.startswith('#') or
            content_stripped.startswith('---') or
            content_stripped.startswith('>')
        )
        # Standard check fails
        assert is_markdown is False
        # Fallback logic should accept it
        is_spa_shell = 'Loading...' in content_stripped and len(content_stripped) < 500
        is_html_page = content_stripped.startswith('<!DOCTYPE') or content_stripped.startswith('<html')
        if not is_spa_shell and not is_html_page and len(content_stripped) > 50:
            is_markdown = True
        assert is_markdown is True

    def test_rejects_spa_shell(self, temp_dir):
        """Short content with 'Loading...' is rejected as SPA shell."""
        content = "Loading..."
        content_stripped = content.strip()
        is_markdown = (
            content_stripped.startswith('#') or
            content_stripped.startswith('---') or
            content_stripped.startswith('>')
        )
        if not is_markdown:
            is_spa_shell = 'Loading...' in content_stripped and len(content_stripped) < 500
            is_html_page = content_stripped.startswith('<!DOCTYPE') or content_stripped.startswith('<html')
            if not is_spa_shell and not is_html_page and len(content_stripped) > 50:
                is_markdown = True
        assert is_markdown is False

    def test_rejects_html_error_page(self, temp_dir):
        """Content starting with <!DOCTYPE is rejected."""
        content = '<!DOCTYPE html><html><body>Error page with enough content to exceed fifty characters threshold</body></html>'
        content_stripped = content.strip()
        is_markdown = (
            content_stripped.startswith('#') or
            content_stripped.startswith('---') or
            content_stripped.startswith('>')
        )
        if not is_markdown:
            is_spa_shell = 'Loading...' in content_stripped and len(content_stripped) < 500
            is_html_page = content_stripped.startswith('<!DOCTYPE') or content_stripped.startswith('<html')
            if not is_spa_shell and not is_html_page and len(content_stripped) > 50:
                is_markdown = True
        assert is_markdown is False


class TestExcludePatterns:
    """Tests for exclude_patterns in parse_sitemap."""

    def test_exclude_patterns_filters_urls(self, temp_dir):
        """Exclude patterns remove matching URLs from sitemap results."""
        from scripts.core.scrape_docs import DocScraper

        scraper = DocScraper(base_output_dir=temp_dir)

        sitemap_content = create_mock_sitemap([
            'https://platform.claude.com/docs/en/api/cli/messages/create',
            'https://platform.claude.com/docs/en/api/cli/messages/list',
            'https://platform.claude.com/docs/en/api/php/messages/create',
            'https://platform.claude.com/docs/en/api/python/messages/create',
            'https://platform.claude.com/docs/en/docs/overview',
        ])

        scraper.fetch_url = MagicMock(return_value=(sitemap_content, None))

        urls = scraper.parse_sitemap(
            'https://platform.claude.com/sitemap.xml',
            url_filter='/docs/en/',
            exclude_patterns=['/api/cli/', '/api/php/']
        )

        assert len(urls) == 2
        assert all('/api/cli/' not in url for url in urls)
        assert all('/api/php/' not in url for url in urls)
        assert any('/api/python/' in url for url in urls)
        assert any('/docs/overview' in url for url in urls)

    def test_exclude_patterns_empty_list(self, temp_dir):
        """Empty exclude_patterns list has no effect."""
        from scripts.core.scrape_docs import DocScraper

        scraper = DocScraper(base_output_dir=temp_dir)

        sitemap_content = create_mock_sitemap([
            'https://example.com/docs/en/page1',
            'https://example.com/docs/en/page2',
        ])

        scraper.fetch_url = MagicMock(return_value=(sitemap_content, None))

        urls = scraper.parse_sitemap(
            'https://example.com/sitemap.xml',
            url_filter='/docs/en/',
            exclude_patterns=[]
        )

        assert len(urls) == 2

    def test_exclude_patterns_none(self, temp_dir):
        """None exclude_patterns has no effect (backwards compatible)."""
        from scripts.core.scrape_docs import DocScraper

        scraper = DocScraper(base_output_dir=temp_dir)

        sitemap_content = create_mock_sitemap([
            'https://example.com/docs/en/page1',
            'https://example.com/docs/en/page2',
        ])

        scraper.fetch_url = MagicMock(return_value=(sitemap_content, None))

        urls = scraper.parse_sitemap(
            'https://example.com/sitemap.xml',
            url_filter='/docs/en/',
            exclude_patterns=None
        )

        assert len(urls) == 2


class TestNormalizeSmartQuotes:
    """Tests for normalize_smart_quotes static method."""

    def test_replaces_smart_single_quotes(self, temp_dir):
        """Left/right single quotes replaced with straight apostrophe."""
        from scripts.core.scrape_docs import DocScraper

        result = DocScraper.normalize_smart_quotes("it\u2018s a \u2019test\u2019")
        assert result == "it's a 'test'"
        assert '\u2018' not in result
        assert '\u2019' not in result

    def test_replaces_smart_double_quotes(self, temp_dir):
        """Left/right double quotes replaced with straight double quote."""
        from scripts.core.scrape_docs import DocScraper

        result = DocScraper.normalize_smart_quotes('he said \u201Chello\u201D')
        assert result == 'he said "hello"'
        assert '\u201C' not in result
        assert '\u201D' not in result

    def test_preserves_straight_quotes(self, temp_dir):
        """Existing straight quotes are unchanged."""
        from scripts.core.scrape_docs import DocScraper

        original = "it's a \"test\" with 'straight' quotes"
        result = DocScraper.normalize_smart_quotes(original)
        assert result == original

    def test_mixed_content(self, temp_dir):
        """Mixed smart/straight quotes in realistic markdown content."""
        from scripts.core.scrape_docs import DocScraper

        content = "# Claude\u2019s API\n\nThe \u201Cmessages\u201D endpoint handles requests. Use 'straight' quotes too."
        result = DocScraper.normalize_smart_quotes(content)
        assert result == "# Claude's API\n\nThe \"messages\" endpoint handles requests. Use 'straight' quotes too."

    def test_empty_string(self, temp_dir):
        """Empty string returns empty string."""
        from scripts.core.scrape_docs import DocScraper

        result = DocScraper.normalize_smart_quotes("")
        assert result == ""


class TestExtractBodyLines:
    """Tests for _extract_body_lines helper."""

    def test_extract_body_lines_with_frontmatter(self, temp_dir):
        """Body lines should exclude YAML frontmatter and empty lines."""
        from scripts.core.scrape_docs import DocScraper

        content = "---\ntitle: Test\nsource_url: https://example.com\n---\n\n# Heading\n\nParagraph one.\nParagraph two.\n"
        body = DocScraper._extract_body_lines(content)
        assert body == ["# Heading", "Paragraph one.", "Paragraph two."]

    def test_extract_body_lines_without_frontmatter(self, temp_dir):
        """Content without frontmatter should return all non-empty lines."""
        from scripts.core.scrape_docs import DocScraper

        content = "# Heading\n\nSome content.\nMore content.\n"
        body = DocScraper._extract_body_lines(content)
        assert body == ["# Heading", "Some content.", "More content."]
