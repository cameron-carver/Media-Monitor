"""
Matching strategies for company name detection.

Different companies require different matching strategies based on
name uniqueness. This module provides matcher implementations for
each strategy type.
"""

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from difflib import SequenceMatcher
from typing import Optional

from ..config.companies import Company, SensitivityProfile


@dataclass
class Match:
    """A potential company mention found in text."""

    # The matched text
    text: str

    # Start position in the source text
    start: int

    # End position in the source text
    end: int

    # Which name variant matched (primary name, alias, or ticker)
    matched_name: str

    # Initial confidence from the matching strategy (0.0 - 1.0)
    base_confidence: float

    # Context around the match
    context_before: str = ""
    context_after: str = ""


@dataclass
class MatchResult:
    """Result of matching with confidence adjustments."""

    match: Match

    # Final confidence after all adjustments
    final_confidence: float

    # Context keywords found
    context_keywords_found: list[str]

    # Negative keywords found (reduce confidence)
    negative_keywords_found: list[str]

    # Whether this match passes the minimum confidence threshold
    is_valid: bool

    # Explanation of confidence calculation
    explanation: str


class BaseMatcher(ABC):
    """Abstract base class for company name matchers."""

    @abstractmethod
    def find_matches(self, text: str, company: Company) -> list[Match]:
        """Find all potential matches for a company in the text."""
        pass

    def _extract_context(self, text: str, start: int, end: int, window: int = 50) -> tuple[str, str]:
        """Extract context around a match position."""
        context_start = max(0, start - window)
        context_end = min(len(text), end + window)

        before = text[context_start:start].strip()
        after = text[end:context_end].strip()

        return before, after


class ExactMatcher(BaseMatcher):
    """Matches company names with exact case-sensitive matching."""

    def find_matches(self, text: str, company: Company) -> list[Match]:
        matches = []
        names = company.get_all_names()

        for name in names:
            # Use word boundary matching to avoid partial matches
            pattern = r'\b' + re.escape(name) + r'\b'

            for m in re.finditer(pattern, text):
                before, after = self._extract_context(
                    text, m.start(), m.end(),
                    company.sensitivity.context_window if company.sensitivity else 50
                )
                matches.append(Match(
                    text=m.group(),
                    start=m.start(),
                    end=m.end(),
                    matched_name=name,
                    base_confidence=1.0,  # Exact match = full base confidence
                    context_before=before,
                    context_after=after,
                ))

        return matches


class CaseInsensitiveMatcher(BaseMatcher):
    """Matches company names with case-insensitive matching."""

    def find_matches(self, text: str, company: Company) -> list[Match]:
        matches = []
        names = company.get_all_names()

        for name in names:
            pattern = r'\b' + re.escape(name) + r'\b'

            for m in re.finditer(pattern, text, re.IGNORECASE):
                # Reduce confidence slightly if case doesn't match
                is_exact_case = m.group() == name
                confidence = 1.0 if is_exact_case else 0.95

                before, after = self._extract_context(
                    text, m.start(), m.end(),
                    company.sensitivity.context_window if company.sensitivity else 50
                )
                matches.append(Match(
                    text=m.group(),
                    start=m.start(),
                    end=m.end(),
                    matched_name=name,
                    base_confidence=confidence,
                    context_before=before,
                    context_after=after,
                ))

        return matches


class FuzzyMatcher(BaseMatcher):
    """Matches company names with fuzzy matching for typos."""

    def __init__(self, min_similarity: float = 0.85):
        self.min_similarity = min_similarity

    def find_matches(self, text: str, company: Company) -> list[Match]:
        matches = []
        names = company.get_all_names()

        # Split text into words and check each word/phrase
        words = text.split()

        for name in names:
            name_word_count = len(name.split())

            # Check single words and multi-word phrases
            for i in range(len(words)):
                for length in range(1, min(name_word_count + 1, len(words) - i + 1)):
                    candidate = ' '.join(words[i:i + length])

                    # Calculate similarity
                    similarity = SequenceMatcher(
                        None,
                        name.lower(),
                        candidate.lower()
                    ).ratio()

                    if similarity >= self.min_similarity:
                        # Find position in original text
                        start = text.lower().find(candidate.lower())
                        if start == -1:
                            continue

                        end = start + len(candidate)
                        before, after = self._extract_context(
                            text, start, end,
                            company.sensitivity.context_window if company.sensitivity else 50
                        )

                        matches.append(Match(
                            text=candidate,
                            start=start,
                            end=end,
                            matched_name=name,
                            base_confidence=similarity,
                            context_before=before,
                            context_after=after,
                        ))

        # Deduplicate overlapping matches, keeping highest confidence
        return self._deduplicate_matches(matches)

    def _deduplicate_matches(self, matches: list[Match]) -> list[Match]:
        """Remove overlapping matches, keeping the highest confidence."""
        if not matches:
            return []

        # Sort by confidence descending
        sorted_matches = sorted(matches, key=lambda m: m.base_confidence, reverse=True)
        result = []

        for match in sorted_matches:
            # Check if this overlaps with any already-selected match
            overlaps = False
            for selected in result:
                if (match.start < selected.end and match.end > selected.start):
                    overlaps = True
                    break

            if not overlaps:
                result.append(match)

        return result


class ContextualMatcher(CaseInsensitiveMatcher):
    """
    Matches company names and requires contextual signals.

    Used for ambiguous names that need supporting context.
    """

    def __init__(self, context_boost: float = 0.15):
        self.context_boost = context_boost

    def find_matches(self, text: str, company: Company) -> list[Match]:
        # First get case-insensitive matches
        matches = super().find_matches(text, company)

        # For contextual matching, we start with lower base confidence
        # and rely on context analysis to boost it
        for match in matches:
            match.base_confidence *= 0.7  # Reduce initial confidence

        return matches


class StrictMatcher(BaseMatcher):
    """
    Strictest matching for common-word company names.

    Requires exact or near-exact match plus additional signals.
    """

    def find_matches(self, text: str, company: Company) -> list[Match]:
        matches = []
        names = company.get_all_names()

        for name in names:
            # For strict matching, prefer capitalized versions
            # Look for the name with proper capitalization
            pattern = r'\b' + re.escape(name) + r'\b'

            for m in re.finditer(pattern, text):
                # Check if it's properly capitalized (like a proper noun)
                matched_text = m.group()
                is_capitalized = matched_text[0].isupper()

                # Strict matcher starts with lower base confidence
                # for common words
                if is_capitalized:
                    confidence = 0.6  # Capitalized = more likely company
                else:
                    confidence = 0.3  # Lowercase = likely just the word

                before, after = self._extract_context(
                    text, m.start(), m.end(),
                    company.sensitivity.context_window if company.sensitivity else 50
                )

                matches.append(Match(
                    text=matched_text,
                    start=m.start(),
                    end=m.end(),
                    matched_name=name,
                    base_confidence=confidence,
                    context_before=before,
                    context_after=after,
                ))

        return matches


def get_matcher(profile: SensitivityProfile) -> BaseMatcher:
    """Get the appropriate matcher for a sensitivity profile."""
    from ..config.companies import MatchingStrategy

    matchers = {
        MatchingStrategy.EXACT: ExactMatcher(),
        MatchingStrategy.CASE_INSENSITIVE: CaseInsensitiveMatcher(),
        MatchingStrategy.FUZZY: FuzzyMatcher(),
        MatchingStrategy.CONTEXTUAL: ContextualMatcher(),
        MatchingStrategy.STRICT: StrictMatcher(),
    }

    return matchers.get(profile.matching_strategy, CaseInsensitiveMatcher())
