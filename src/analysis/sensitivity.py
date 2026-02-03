"""
Sensitivity Analysis Engine

This module provides company-aware sensitivity analysis that adapts
matching behavior based on how unique each company's name is.

Companies with common-word names (Apple, Target, Delta) require stricter
matching with contextual signals, while companies with unique names
(Anthropic, Palantir) can use more relaxed matching.
"""

import re
from dataclasses import dataclass, field
from typing import Optional

from ..config.companies import Company, SensitivityProfile, NameUniqueness
from .matchers import Match, MatchResult, get_matcher


@dataclass
class CompanyMention:
    """A validated company mention in analyzed text."""

    company: Company
    match_result: MatchResult
    sentiment: Optional[str] = None  # positive, negative, neutral
    sentiment_confidence: Optional[float] = None


@dataclass
class AnalysisResult:
    """Complete analysis result for a piece of text."""

    # The analyzed text
    text: str

    # All company mentions found
    mentions: list[CompanyMention] = field(default_factory=list)

    # Companies analyzed
    companies_checked: list[str] = field(default_factory=list)

    # Analysis metadata
    total_matches_found: int = 0
    valid_matches: int = 0
    rejected_matches: int = 0

    def get_mentions_by_company(self, company_id: str) -> list[CompanyMention]:
        """Get all mentions for a specific company."""
        return [m for m in self.mentions if m.company.id == company_id]

    def get_high_confidence_mentions(self, min_confidence: float = 0.8) -> list[CompanyMention]:
        """Get mentions above a confidence threshold."""
        return [
            m for m in self.mentions
            if m.match_result.final_confidence >= min_confidence
        ]


class SensitivityAnalyzer:
    """
    Company-aware sensitivity analyzer.

    This analyzer applies different matching strategies based on company
    name uniqueness. It handles:

    - COMMON_WORD names: Strict matching with required context
    - AMBIGUOUS names: Context-enhanced matching
    - MODERATE names: Standard case-insensitive matching
    - UNIQUE names: Relaxed fuzzy matching
    """

    def __init__(
        self,
        companies: list[Company],
        default_min_confidence: float = 0.7,
    ):
        """
        Initialize the analyzer with companies to monitor.

        Args:
            companies: List of companies to analyze for
            default_min_confidence: Default minimum confidence threshold
        """
        self.companies = {c.id: c for c in companies}
        self.default_min_confidence = default_min_confidence

    def analyze(self, text: str, company_ids: list[str] | None = None) -> AnalysisResult:
        """
        Analyze text for company mentions.

        Args:
            text: The text to analyze
            company_ids: Optional list of company IDs to check.
                        If None, checks all registered companies.

        Returns:
            AnalysisResult with all found mentions
        """
        result = AnalysisResult(text=text)

        # Determine which companies to check
        if company_ids:
            companies_to_check = [
                self.companies[cid] for cid in company_ids
                if cid in self.companies
            ]
        else:
            companies_to_check = list(self.companies.values())

        result.companies_checked = [c.id for c in companies_to_check]

        # Analyze each company
        for company in companies_to_check:
            mentions = self._analyze_company(text, company)
            result.mentions.extend(mentions)
            result.total_matches_found += len(mentions)

        # Count valid vs rejected
        result.valid_matches = len([m for m in result.mentions if m.match_result.is_valid])
        result.rejected_matches = result.total_matches_found - result.valid_matches

        # Filter to only valid mentions
        result.mentions = [m for m in result.mentions if m.match_result.is_valid]

        return result

    def _analyze_company(self, text: str, company: Company) -> list[CompanyMention]:
        """Analyze text for a single company's mentions."""
        if not company.sensitivity:
            return []

        # Get appropriate matcher for this company's sensitivity profile
        matcher = get_matcher(company.sensitivity)

        # Find all potential matches
        matches = matcher.find_matches(text, company)

        # Evaluate each match with context analysis
        mentions = []
        for match in matches:
            match_result = self._evaluate_match(match, company)
            mentions.append(CompanyMention(
                company=company,
                match_result=match_result,
            ))

        return mentions

    def _evaluate_match(self, match: Match, company: Company) -> MatchResult:
        """
        Evaluate a match and calculate final confidence.

        This applies context-based confidence adjustments based on
        the company's sensitivity profile.
        """
        profile = company.sensitivity
        confidence = match.base_confidence
        explanations = [f"Base confidence: {match.base_confidence:.2f}"]

        # Combine context for searching
        full_context = f"{match.context_before} {match.text} {match.context_after}".lower()

        # Check for context keywords (boost confidence)
        context_keywords_found = []
        if profile.context_keywords:
            for keyword in profile.context_keywords:
                if keyword.lower() in full_context:
                    context_keywords_found.append(keyword)

            if context_keywords_found:
                # Boost based on number of keywords found
                # Common-word companies get bigger boosts from context
                if profile.uniqueness == NameUniqueness.COMMON_WORD:
                    keyword_boost = min(0.4, len(context_keywords_found) * 0.1)
                else:
                    keyword_boost = min(0.3, len(context_keywords_found) * 0.05)
                confidence += keyword_boost
                explanations.append(
                    f"Context keywords found ({len(context_keywords_found)}): +{keyword_boost:.2f}"
                )

        # Check for negative keywords (reduce confidence)
        negative_keywords_found = []
        if profile.negative_keywords:
            for keyword in profile.negative_keywords:
                if keyword.lower() in full_context:
                    negative_keywords_found.append(keyword)

            if negative_keywords_found:
                # Reduce based on number of negative keywords
                negative_penalty = min(0.4, len(negative_keywords_found) * 0.15)
                confidence -= negative_penalty
                explanations.append(
                    f"Negative keywords found ({len(negative_keywords_found)}): -{negative_penalty:.2f}"
                )

        # For profiles requiring context, penalize if none found
        if profile.require_context and not context_keywords_found:
            context_penalty = 0.25
            confidence -= context_penalty
            explanations.append(f"Required context not found: -{context_penalty:.2f}")

        # Apply uniqueness-based adjustments
        confidence = self._apply_uniqueness_adjustments(
            confidence, match, company, explanations
        )

        # Clamp confidence to valid range
        confidence = max(0.0, min(1.0, confidence))
        explanations.append(f"Final confidence: {confidence:.2f}")

        # Determine if valid
        min_conf = profile.min_confidence
        is_valid = confidence >= min_conf

        if not is_valid:
            explanations.append(f"REJECTED: Below threshold ({min_conf:.2f})")

        return MatchResult(
            match=match,
            final_confidence=confidence,
            context_keywords_found=context_keywords_found,
            negative_keywords_found=negative_keywords_found,
            is_valid=is_valid,
            explanation=" | ".join(explanations),
        )

    def _apply_uniqueness_adjustments(
        self,
        confidence: float,
        match: Match,
        company: Company,
        explanations: list[str],
    ) -> float:
        """Apply confidence adjustments based on name uniqueness."""
        profile = company.sensitivity
        uniqueness = profile.uniqueness

        if uniqueness == NameUniqueness.COMMON_WORD:
            # For common words, check if it looks like a proper noun usage
            # (surrounded by business/financial context)
            business_patterns = [
                r'\b(stock|shares|Inc|Corp|CEO|earnings|quarterly|revenue)\b',
                r'\$[\d,]+',  # Dollar amounts
                r'\b\d+%\b',  # Percentages
            ]

            context = f"{match.context_before} {match.context_after}"
            business_signals = sum(
                1 for pattern in business_patterns
                if re.search(pattern, context, re.IGNORECASE)
            )

            if business_signals > 0:
                boost = min(0.25, business_signals * 0.1)
                confidence += boost
                explanations.append(f"Business context signals ({business_signals}): +{boost:.2f}")
            else:
                penalty = 0.15
                confidence -= penalty
                explanations.append(f"No business context for common word: -{penalty:.2f}")

        elif uniqueness == NameUniqueness.AMBIGUOUS:
            # For ambiguous names, check if full company name is used
            if match.matched_name == company.name:
                boost = 0.1
                confidence += boost
                explanations.append(f"Full company name matched: +{boost:.2f}")

        elif uniqueness == NameUniqueness.UNIQUE:
            # For unique names, boost slightly as false positives are rare
            boost = 0.05
            confidence += boost
            explanations.append(f"Unique company name bonus: +{boost:.2f}")

        return confidence

    def get_sensitivity_summary(self) -> dict:
        """Get a summary of sensitivity settings for all companies."""
        summary = {
            "total_companies": len(self.companies),
            "by_uniqueness": {},
            "by_strategy": {},
        }

        for company in self.companies.values():
            if company.sensitivity:
                # Count by uniqueness
                uniq = company.sensitivity.uniqueness.value
                summary["by_uniqueness"][uniq] = summary["by_uniqueness"].get(uniq, 0) + 1

                # Count by strategy
                strat = company.sensitivity.matching_strategy.value
                summary["by_strategy"][strat] = summary["by_strategy"].get(strat, 0) + 1

        return summary


def create_analyzer_from_registry() -> SensitivityAnalyzer:
    """Create an analyzer with all companies from the registry."""
    from ..config.company_registry import get_all_companies
    return SensitivityAnalyzer(get_all_companies())
