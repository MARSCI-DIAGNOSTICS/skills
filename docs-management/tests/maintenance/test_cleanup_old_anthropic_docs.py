"""
Tests for cleanup_old_anthropic_docs.py script.

Tests the cleanup_old_anthropic_docs.py script for removing old Anthropic documentation.
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta


import pytest
from tests.shared.test_utils import TempReferencesDir, create_mock_index_entry



class TestCleanupOldAnthropicDocs:
    """Test suite for cleanup_old_anthropic_docs.py."""

    def test_script_imports(self):
        """Test that script can be imported."""
        sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
        
        try:
            from scripts.maintenance import cleanup_old_anthropic_docs
            assert True
        except ImportError:
            pytest.fail("cleanup_old_anthropic_docs.py could not be imported")

    def test_cleanup_old_docs_function_exists(self, temp_dir):
        """Test that cleanup_old_docs function exists."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.maintenance.cleanup_old_anthropic_docs import cleanup_old_docs
            
            # Should not raise
            result = cleanup_old_docs(refs_dir.references_dir, max_age_days=365, dry_run=True)
            assert isinstance(result, int)
            
        finally:
            refs_dir.cleanup()

    def test_cleanup_old_docs_dry_run(self):
        """Test cleanup_old_docs in dry-run mode."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.maintenance.cleanup_old_anthropic_docs import cleanup_old_docs
            
            # Create old doc entry
            old_date = (datetime.now() - timedelta(days=400)).strftime('%Y-%m-%d')
            index = {
                'test-doc': create_mock_index_entry(
                    'test-doc',
                    'https://anthropic.com/test',
                    'anthropic-com/test.md',
                    domain='anthropic.com',
                    category='engineering',
                    published_at=old_date
                )
            }
            
            # Create index file
            refs_dir.create_index(index)
            
            # Create doc file
            refs_dir.create_doc('anthropic-com', 'engineering', 'test.md', '# Test')
            
            # Run cleanup in dry-run mode
            result = cleanup_old_docs(refs_dir.references_dir, max_age_days=365, dry_run=True)
            
            # Should return 0 (success) in dry-run
            assert result == 0
            
            # File should still exist (dry-run)
            doc_file = refs_dir.references_dir / 'anthropic-com' / 'engineering' / 'test.md'
            assert doc_file.exists()
            
        finally:
            refs_dir.cleanup()

    def test_cleanup_old_docs_skips_recent_docs(self):
        """Test that recent docs are not cleaned up."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.maintenance.cleanup_old_anthropic_docs import cleanup_old_docs
            
            # Create recent doc entry
            recent_date = (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d')
            index = {
                'test-doc': create_mock_index_entry(
                    'test-doc',
                    'https://anthropic.com/test',
                    'anthropic-com/test.md',
                    domain='anthropic.com',
                    category='engineering',
                    published_at=recent_date
                )
            }
            
            refs_dir.create_index(index)
            refs_dir.create_doc('anthropic-com', 'engineering', 'test.md', '# Test')
            
            # Run cleanup
            result = cleanup_old_docs(refs_dir.references_dir, max_age_days=365, dry_run=True)
            
            # Should return 0 (no old docs found)
            assert result == 0
            
        finally:
            refs_dir.cleanup()

    def test_cleanup_old_docs_execute_mode(self):
        """Test cleanup_old_docs actually deletes files in execute mode."""
        refs_dir = TempReferencesDir()

        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.maintenance.cleanup_old_anthropic_docs import cleanup_old_docs

            # Create old doc entry (400 days old)
            old_date = (datetime.now() - timedelta(days=400)).strftime('%Y-%m-%d')
            index = {
                'test-doc': create_mock_index_entry(
                    'test-doc',
                    'https://anthropic.com/test',
                    'anthropic-com/engineering/test.md',
                    domain='anthropic.com',
                    category='engineering',
                    published_at=old_date
                )
            }

            refs_dir.create_index(index)
            doc_file = refs_dir.create_doc('anthropic-com', 'engineering', 'test.md', '# Old Test Doc')

            # Verify file exists before cleanup
            assert doc_file.exists()

            # Run cleanup in execute mode (dry_run=False)
            result = cleanup_old_docs(refs_dir.references_dir, max_age_days=365, dry_run=False)

            # Should have deleted 1 file
            assert result == 1

            # File should be deleted
            assert not doc_file.exists()

            # Entry should be removed from index
            from scripts.management.index_manager import IndexManager
            manager = IndexManager(refs_dir.references_dir)
            entry = manager.get_entry('test-doc')
            assert entry is None, "Entry should be removed from index after cleanup"

        finally:
            refs_dir.cleanup()

    def test_cleanup_old_docs_uses_180_day_threshold(self):
        """Test that cleanup correctly uses custom age thresholds."""
        refs_dir = TempReferencesDir()

        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.maintenance.cleanup_old_anthropic_docs import cleanup_old_docs

            # Create doc 190 days old (should be flagged with max_age_days=180)
            old_date = (datetime.now() - timedelta(days=190)).strftime('%Y-%m-%d')
            # Create doc 170 days old (should NOT be flagged with max_age_days=180)
            recent_date = (datetime.now() - timedelta(days=170)).strftime('%Y-%m-%d')

            index = {
                'old-doc': create_mock_index_entry(
                    'old-doc',
                    'https://anthropic.com/old',
                    'anthropic-com/news/old.md',
                    domain='anthropic.com',
                    category='news',
                    published_at=old_date
                ),
                'recent-doc': create_mock_index_entry(
                    'recent-doc',
                    'https://anthropic.com/recent',
                    'anthropic-com/news/recent.md',
                    domain='anthropic.com',
                    category='news',
                    published_at=recent_date
                ),
            }

            refs_dir.create_index(index)
            refs_dir.create_doc('anthropic-com', 'news', 'old.md', '# Old Doc')
            refs_dir.create_doc('anthropic-com', 'news', 'recent.md', '# Recent Doc')

            # Run cleanup with 180-day threshold in dry-run mode
            # The function returns 0 in dry-run, but prints findings
            # Run in execute mode to verify only the old doc is deleted
            result = cleanup_old_docs(refs_dir.references_dir, max_age_days=180, dry_run=False)

            # Should delete only the 190-day-old doc
            assert result == 1

            # Old doc file should be deleted
            old_file = refs_dir.references_dir / 'anthropic-com' / 'news' / 'old.md'
            assert not old_file.exists(), "190-day-old doc should be deleted"

            # Recent doc file should still exist
            recent_file = refs_dir.references_dir / 'anthropic-com' / 'news' / 'recent.md'
            assert recent_file.exists(), "170-day-old doc should NOT be deleted"

        finally:
            refs_dir.cleanup()

    def test_cleanup_old_docs_skips_non_anthropic_docs(self):
        """Test that non-Anthropic docs are not cleaned up."""
        refs_dir = TempReferencesDir()
        
        try:
            sys.path.insert(0, str(Path(__file__).parent.parent / 'scripts'))
            from scripts.maintenance.cleanup_old_anthropic_docs import cleanup_old_docs
            
            # Create old doc entry for non-Anthropic domain
            old_date = (datetime.now() - timedelta(days=400)).strftime('%Y-%m-%d')
            index = {
                'test-doc': create_mock_index_entry(
                    'test-doc',
                    'https://docs.claude.com/test',
                    'docs-claude-com/test.md',
                    domain='docs.claude.com',
                    category='api',
                    published_at=old_date
                )
            }
            
            refs_dir.create_index(index)
            refs_dir.create_doc('docs-claude-com', 'api', 'test.md', '# Test')
            
            # Run cleanup
            result = cleanup_old_docs(refs_dir.references_dir, max_age_days=365, dry_run=True)
            
            # Should return 0 (no Anthropic docs found)
            assert result == 0
            
        finally:
            refs_dir.cleanup()
