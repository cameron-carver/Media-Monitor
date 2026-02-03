"""
Company configuration with per-company sensitivity settings.

Companies are classified by name uniqueness to determine appropriate
matching strategies. A company like "Apple" requires stricter matching
than "Anthropic" since "apple" is a common English word.
"""

from enum import Enum
from dataclasses import dataclass, field
from typing import Optional


class NameUniqueness(Enum):
    """Classification of how unique a company name is."""

    # Name is a common word or phrase (e.g., "Apple", "Target", "Amazon")
    COMMON_WORD = "common_word"

    # Name is a common name or could refer to multiple entities (e.g., "Goldman", "Morgan")
    AMBIGUOUS = "ambiguous"

    # Name is somewhat unique but has some overlap potential (e.g., "Microsoft", "Google")
    MODERATE = "moderate"

    # Name is highly unique/distinctive (e.g., "Anthropic", "Palantir", "Snowflake")
    UNIQUE = "unique"


class MatchingStrategy(Enum):
    """Strategy for matching company mentions in text."""

    # Require exact match with proper capitalization
    EXACT = "exact"

    # Match with case insensitivity but exact spelling
    CASE_INSENSITIVE = "case_insensitive"

    # Allow fuzzy matching for typos
    FUZZY = "fuzzy"

    # Require contextual signals (industry terms, etc.)
    CONTEXTUAL = "contextual"

    # Require multiple signals (name + context + proximity to keywords)
    STRICT = "strict"


@dataclass
class SensitivityProfile:
    """Sensitivity settings for a specific company."""

    # How unique is the company name?
    uniqueness: NameUniqueness

    # Primary matching strategy
    matching_strategy: MatchingStrategy

    # Minimum confidence score (0.0 - 1.0) required for a match
    min_confidence: float = 0.7

    # Require context keywords nearby?
    require_context: bool = False

    # Keywords that increase confidence when found nearby
    context_keywords: list[str] = field(default_factory=list)

    # Keywords that decrease confidence (false positive signals)
    negative_keywords: list[str] = field(default_factory=list)

    # How many words of context to check around a potential match
    context_window: int = 50

    # Weight multiplier for this company in aggregated analysis
    weight: float = 1.0


@dataclass
class Company:
    """Company definition with all relevant matching information."""

    # Unique identifier
    id: str

    # Primary/official company name
    name: str

    # Ticker symbol if publicly traded
    ticker: Optional[str] = None

    # Alternative names, abbreviations, common misspellings
    aliases: list[str] = field(default_factory=list)

    # Industry sector
    sector: Optional[str] = None

    # Sensitivity profile for this company
    sensitivity: Optional[SensitivityProfile] = None

    def __post_init__(self):
        """Set default sensitivity if not provided."""
        if self.sensitivity is None:
            self.sensitivity = self._infer_sensitivity()

    def _infer_sensitivity(self) -> SensitivityProfile:
        """Infer sensitivity settings based on company name characteristics."""
        # Default to moderate settings
        return SensitivityProfile(
            uniqueness=NameUniqueness.MODERATE,
            matching_strategy=MatchingStrategy.CASE_INSENSITIVE,
            min_confidence=0.7
        )

    def get_all_names(self) -> list[str]:
        """Get all possible names for this company."""
        names = [self.name] + self.aliases
        if self.ticker:
            names.append(self.ticker)
        return names


# Pre-defined sensitivity profiles for common patterns
COMMON_WORD_PROFILE = SensitivityProfile(
    uniqueness=NameUniqueness.COMMON_WORD,
    matching_strategy=MatchingStrategy.STRICT,
    min_confidence=0.85,
    require_context=True,
    context_window=30,
)

AMBIGUOUS_NAME_PROFILE = SensitivityProfile(
    uniqueness=NameUniqueness.AMBIGUOUS,
    matching_strategy=MatchingStrategy.CONTEXTUAL,
    min_confidence=0.75,
    require_context=True,
    context_window=40,
)

MODERATE_PROFILE = SensitivityProfile(
    uniqueness=NameUniqueness.MODERATE,
    matching_strategy=MatchingStrategy.CASE_INSENSITIVE,
    min_confidence=0.7,
    require_context=False,
)

UNIQUE_NAME_PROFILE = SensitivityProfile(
    uniqueness=NameUniqueness.UNIQUE,
    matching_strategy=MatchingStrategy.FUZZY,
    min_confidence=0.6,
    require_context=False,
)
