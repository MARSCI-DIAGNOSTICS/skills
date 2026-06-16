#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
extract_metadata.py - Keyword and tag extraction for blog articles.

Features:
- Keyword extraction (TF-IDF, RAKE, or simple frequency)
- Tag detection from content patterns
- Pattern detection for architecture styles
"""

import re
import sys
from collections import Counter
from pathlib import Path
from typing import Optional

# Add parent to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from bootstrap import skill_dir


class MetadataExtractor:
    """
    Extracts keywords, tags, and patterns from article content.
    """

    # Tag detection patterns
    TAG_PATTERNS = {
        'clean-architecture': [
            r'\bclean\s+architecture\b',
            r'\bonion\s+architecture\b',
            r'\bhexagonal\s+architecture\b',
            r'\bports\s+and\s+adapters\b',
        ],
        'ddd': [
            r'\bdomain[- ]driven\s+design\b',
            r'\bDDD\b',
            r'\bdomain\s+model\b',
            r'\baggregate\s+root\b',
            r'\bvalue\s+object\b',
            r'\bdomain\s+event\b',
            r'\bbounded\s+context\b',
        ],
        'cqrs': [
            r'\bCQRS\b',
            r'\bcommand\s+query\b',
            r'\bcommand\s+handler\b',
            r'\bquery\s+handler\b',
        ],
        'mediatr': [
            r'\bMediatR\b',
            r'\bIRequest\b',
            r'\bIRequestHandler\b',
            r'\bINotification\b',
        ],
        'ef-core': [
            r'\bEntity\s+Framework\b',
            r'\bEF\s+Core\b',
            r'\bDbContext\b',
            r'\bIQueryable\b',
            r'\bDbSet\b',
        ],
        'aspnet-core': [
            r'\bASP\.NET\s+Core\b',
            r'\bMinimal\s+API\b',
            r'\b\[ApiController\]\b',
            r'\bControllerBase\b',
            r'\bMiddleware\b',
        ],
        'modular-monolith': [
            r'\bmodular\s+monolith\b',
            r'\bmodule\s+boundaries\b',
        ],
        'vertical-slice': [
            r'\bvertical\s+slice\b',
            r'\bfeature\s+slice\b',
            r'\bfeature\s+folder\b',
        ],
        'dotnet-10': [
            r'\b\.NET\s+10\b',
            r'\bdotnet\s+10\b',
            r'\bNET10\b',
        ],
        'dotnet-9': [
            r'\b\.NET\s+9\b',
            r'\bdotnet\s+9\b',
            r'\bNET9\b',
        ],
        'result-pattern': [
            r'\bResult\s+pattern\b',
            r'\bResult<T>\b',
            r'\bErrorOr\b',
            r'\bOneOf\b',
        ],
        'outbox-pattern': [
            r'\boutbox\s+pattern\b',
            r'\btransactional\s+outbox\b',
        ],
        'saga-pattern': [
            r'\bsaga\s+pattern\b',
            r'\borchestration\s+saga\b',
            r'\bchoreography\s+saga\b',
        ],
        'specification-pattern': [
            r'\bspecification\s+pattern\b',
            r'\bISpecification\b',
        ],
        'repository-pattern': [
            r'\brepository\s+pattern\b',
            r'\bIRepository\b',
            r'\bgeneric\s+repository\b',
        ],
        'unit-of-work': [
            r'\bunit\s+of\s+work\b',
            r'\bIUnitOfWork\b',
        ],
        'validation': [
            r'\bFluentValidation\b',
            r'\bIValidator\b',
            r'\bValidationResult\b',
        ],
        'logging': [
            r'\bSerilog\b',
            r'\bstructured\s+logging\b',
            r'\bILogger\b',
        ],
        'testing': [
            r'\bunit\s+test\b',
            r'\bintegration\s+test\b',
            r'\bxUnit\b',
            r'\bNUnit\b',
            r'\bTestcontainers\b',
        ],
        'docker': [
            r'\bDocker\b',
            r'\bcontainer\b',
            r'\bDockerfile\b',
        ],
        'aspire': [
            r'\b\.NET\s+Aspire\b',
            r'\bAspire\b',
        ],
    }

    # Pattern detection for architectural patterns
    PATTERN_DETECTORS = {
        'file-scoped-namespaces': r'\bfile-scoped\s+namespace\b',
        'primary-constructors': r'\bprimary\s+constructor\b',
        'records': r'\brecord\s+(class|struct)\b',
        'minimal-apis': r'\bMinimal\s+API\b',
        'global-usings': r'\bglobal\s+using\b',
        'dependency-injection': r'\bAddScoped\b|\bAddTransient\b|\bAddSingleton\b',
        'async-await': r'\basync\s+Task\b|\bawait\b',
        'nullable-reference-types': r'#nullable\s+enable',
        'source-generators': r'\bsource\s+generator\b|\b\[Generator\]\b',
    }

    # Stop words for keyword extraction
    STOP_WORDS = {
        'a', 'an', 'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'as', 'is', 'was', 'are', 'were', 'been',
        'be', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would',
        'could', 'should', 'may', 'might', 'must', 'shall', 'can', 'need',
        'it', 'its', 'this', 'that', 'these', 'those', 'i', 'you', 'he',
        'she', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why',
        'how', 'all', 'each', 'every', 'both', 'few', 'more', 'most', 'other',
        'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so',
        'than', 'too', 'very', 'just', 'also', 'now', 'here', 'there',
        'using', 'use', 'used', 'code', 'example', 'following', 'lets',
        'see', 'look', 'way', 'want', 'going', 'need', 'make', 'get',
    }

    def __init__(self):
        self.skill_root = skill_dir

    def extract_keywords(
        self,
        content: str,
        max_keywords: int = 20,
        min_length: int = 3,
    ) -> list[str]:
        """
        Extract keywords from content using frequency analysis.

        Args:
            content: Article content (markdown)
            max_keywords: Maximum number of keywords to return
            min_length: Minimum word length

        Returns:
            List of keywords sorted by frequency
        """
        # Remove code blocks
        content = re.sub(r'```[\s\S]*?```', '', content)
        content = re.sub(r'`[^`]+`', '', content)

        # Remove URLs
        content = re.sub(r'https?://\S+', '', content)

        # Remove markdown syntax
        content = re.sub(r'[#*_\[\]\(\){}]', ' ', content)

        # Tokenize
        words = re.findall(r'\b[a-zA-Z][a-zA-Z0-9]*\b', content.lower())

        # Filter
        words = [
            w for w in words
            if len(w) >= min_length
            and w not in self.STOP_WORDS
        ]

        # Count frequencies
        counter = Counter(words)

        # Get top keywords
        keywords = [word for word, _ in counter.most_common(max_keywords)]

        return keywords

    def detect_tags(self, content: str) -> list[str]:
        """
        Detect tags from content using pattern matching.

        Args:
            content: Article content (markdown)

        Returns:
            List of detected tags
        """
        tags = []
        content_lower = content.lower()

        for tag, patterns in self.TAG_PATTERNS.items():
            for pattern in patterns:
                if re.search(pattern, content, re.IGNORECASE):
                    tags.append(tag)
                    break  # Only add tag once

        return sorted(set(tags))

    def detect_patterns(self, content: str) -> list[str]:
        """
        Detect architectural patterns from content.

        Args:
            content: Article content (markdown)

        Returns:
            List of detected patterns
        """
        patterns = []

        for pattern_name, regex in self.PATTERN_DETECTORS.items():
            if re.search(regex, content, re.IGNORECASE):
                patterns.append(pattern_name)

        return sorted(patterns)

    def extract_all(self, content: str) -> dict:
        """
        Extract all metadata from content.

        Args:
            content: Article content (markdown)

        Returns:
            Dict with keywords, tags, patterns
        """
        return {
            'keywords': self.extract_keywords(content),
            'tags': self.detect_tags(content),
            'patterns': self.detect_patterns(content),
        }


def main():
    """CLI for metadata extraction."""
    import argparse
    import json

    parser = argparse.ArgumentParser(
        description='Extract metadata from article content',
    )
    parser.add_argument(
        'file',
        type=Path,
        help='Markdown file to analyze',
    )
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output as JSON',
    )

    args = parser.parse_args()

    if not args.file.exists():
        print(f"File not found: {args.file}", file=sys.stderr)
        sys.exit(1)

    content = args.file.read_text(encoding='utf-8')
    extractor = MetadataExtractor()
    metadata = extractor.extract_all(content)

    if args.json:
        print(json.dumps(metadata, indent=2))
    else:
        print(f"Keywords ({len(metadata['keywords'])}):")
        for kw in metadata['keywords']:
            print(f"  - {kw}")
        print()
        print(f"Tags ({len(metadata['tags'])}):")
        for tag in metadata['tags']:
            print(f"  - {tag}")
        print()
        print(f"Patterns ({len(metadata['patterns'])}):")
        for pattern in metadata['patterns']:
            print(f"  - {pattern}")


if __name__ == '__main__':
    main()
