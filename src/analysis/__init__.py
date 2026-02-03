"""Analysis module for Media Monitor."""

from .sensitivity import SensitivityAnalyzer, MatchResult, AnalysisResult
from .matchers import (
    BaseMatcher,
    ExactMatcher,
    CaseInsensitiveMatcher,
    FuzzyMatcher,
    ContextualMatcher,
    StrictMatcher,
)

__all__ = [
    "SensitivityAnalyzer",
    "MatchResult",
    "AnalysisResult",
    "BaseMatcher",
    "ExactMatcher",
    "CaseInsensitiveMatcher",
    "FuzzyMatcher",
    "ContextualMatcher",
    "StrictMatcher",
]
