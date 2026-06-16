"""
pytest configuration and fixtures for duende-docs tests.
"""
import sys
import tempfile
from pathlib import Path

import pytest


# Add scripts directories to Python path for imports
# The scripts have complex import patterns - we need both scripts/ and scripts/core/
scripts_dir = Path(__file__).resolve().parents[1] / 'scripts'
sys.path.insert(0, str(scripts_dir))
sys.path.insert(0, str(scripts_dir / 'core'))


@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)


@pytest.fixture
def mock_duende_page():
    """Create a mock DuendePage object for testing."""
    # Import here to avoid issues with path setup
    from llms_full_parser import DuendePage

    return DuendePage(
        title="Test Document",
        content="This is test content for the document.",
        source_url="https://docs.duendesoftware.com/test/",
        category="identityserver",
        doc_id="test-doc"
    )


@pytest.fixture
def mock_canonical_dir(temp_dir):
    """Create a mock canonical directory structure."""
    canonical_dir = temp_dir / "canonical"
    canonical_dir.mkdir()

    # Create duendesoftware-com subdirectory
    domain_dir = canonical_dir / "duendesoftware-com"
    domain_dir.mkdir()

    return canonical_dir
