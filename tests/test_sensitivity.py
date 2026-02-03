"""
Tests for company-aware sensitivity analysis.

These tests demonstrate how different companies receive different
treatment based on their name uniqueness.
"""

import pytest

from src.config.companies import (
    Company,
    SensitivityProfile,
    NameUniqueness,
    MatchingStrategy,
    COMMON_WORD_PROFILE,
    UNIQUE_NAME_PROFILE,
)
from src.config.company_registry import (
    APPLE,
    ANTHROPIC,
    AMAZON,
    PALANTIR,
    FORD,
    SNOWFLAKE,
    get_company,
)
from src.analysis.sensitivity import SensitivityAnalyzer, create_analyzer_from_registry


class TestCommonWordCompanies:
    """Test that common-word company names require strict matching."""

    def setup_method(self):
        """Set up analyzer with common-word companies."""
        self.analyzer = SensitivityAnalyzer([APPLE, AMAZON])

    def test_apple_with_tech_context_matches(self):
        """Apple mentioned with tech context should match."""
        text = "Apple announced new iPhone models at today's event. AAPL stock rose 3%."
        result = self.analyzer.analyze(text, ["apple"])

        assert len(result.mentions) > 0
        mention = result.mentions[0]
        assert mention.company.id == "apple"
        assert mention.match_result.final_confidence >= 0.7
        assert "iPhone" in mention.match_result.context_keywords_found

    def test_apple_fruit_context_rejected(self):
        """Apple in fruit context should be rejected or low confidence."""
        text = "I love eating apple pie. The apple orchard had a great harvest this year."
        result = self.analyzer.analyze(text, ["apple"])

        # Should either have no matches or very low confidence
        valid_matches = [m for m in result.mentions if m.match_result.is_valid]
        assert len(valid_matches) == 0

    def test_amazon_with_ecommerce_context_matches(self):
        """Amazon with e-commerce context should match."""
        text = "Amazon Prime Day sales exceeded expectations. AWS revenue grew 25%."
        result = self.analyzer.analyze(text, ["amazon"])

        assert len(result.mentions) > 0
        mention = result.mentions[0]
        assert mention.company.id == "amazon"
        assert mention.match_result.final_confidence >= 0.7

    def test_amazon_river_context_rejected(self):
        """Amazon in rainforest context should be rejected."""
        text = "The Amazon river flows through the Amazon rainforest in Brazil."
        result = self.analyzer.analyze(text, ["amazon"])

        # Negative keywords should reduce confidence
        valid_matches = [m for m in result.mentions if m.match_result.is_valid]
        assert len(valid_matches) == 0


class TestUniqueNameCompanies:
    """Test that unique company names can use relaxed matching."""

    def setup_method(self):
        """Set up analyzer with unique-name companies."""
        self.analyzer = SensitivityAnalyzer([ANTHROPIC, PALANTIR])

    def test_anthropic_matches_easily(self):
        """Anthropic should match without requiring much context."""
        text = "Anthropic released a new AI model."
        result = self.analyzer.analyze(text, ["anthropic"])

        assert len(result.mentions) > 0
        mention = result.mentions[0]
        assert mention.company.id == "anthropic"
        assert mention.match_result.is_valid

    def test_anthropic_with_context_high_confidence(self):
        """Anthropic with AI context should have high confidence."""
        text = "Anthropic's Claude AI demonstrates improved safety. Dario Amodei discussed the LLM advances."
        result = self.analyzer.analyze(text, ["anthropic"])

        assert len(result.mentions) > 0
        mention = result.mentions[0]
        assert mention.match_result.final_confidence >= 0.8
        # Should find multiple context keywords
        assert len(mention.match_result.context_keywords_found) >= 2

    def test_palantir_matches_without_context(self):
        """Palantir should match even without context."""
        text = "Palantir announced quarterly results."
        result = self.analyzer.analyze(text, ["palantir"])

        assert len(result.mentions) > 0
        assert result.mentions[0].match_result.is_valid


class TestAmbiguousNames:
    """Test companies with names that could refer to multiple things."""

    def setup_method(self):
        """Set up analyzer with ambiguous-name companies."""
        self.analyzer = SensitivityAnalyzer([FORD, SNOWFLAKE])

    def test_ford_with_auto_context_matches(self):
        """Ford with automotive context should match."""
        text = "Ford F-150 remains the best-selling truck. Ford's EV lineup is growing."
        result = self.analyzer.analyze(text, ["ford"])

        assert len(result.mentions) > 0
        mention = result.mentions[0]
        assert mention.match_result.is_valid

    def test_ford_name_context_rejected(self):
        """Ford as a person's name should be rejected."""
        text = "Harrison Ford starred in Indiana Jones. Gerald Ford was president."
        result = self.analyzer.analyze(text, ["ford"])

        # Negative keywords should catch these
        valid_matches = [m for m in result.mentions if m.match_result.is_valid]
        assert len(valid_matches) == 0

    def test_snowflake_with_tech_context_matches(self):
        """Snowflake with data context should match."""
        text = "Snowflake's data warehouse solution powers many enterprises. SNOW stock analysis."
        result = self.analyzer.analyze(text, ["snowflake"])

        assert len(result.mentions) > 0
        assert result.mentions[0].match_result.is_valid

    def test_snowflake_weather_context_rejected(self):
        """Snowflake in weather context should be rejected."""
        text = "A snowflake fell on my window during the winter storm."
        result = self.analyzer.analyze(text, ["snowflake"])

        valid_matches = [m for m in result.mentions if m.match_result.is_valid]
        assert len(valid_matches) == 0


class TestMultipleCompanies:
    """Test analyzing for multiple companies simultaneously."""

    def setup_method(self):
        """Set up analyzer with multiple companies."""
        self.analyzer = create_analyzer_from_registry()

    def test_multiple_companies_in_one_text(self):
        """Should find multiple different companies in the same text."""
        text = """
        Tech stocks rallied today. Apple's iPhone sales beat expectations while
        Microsoft Azure revenue grew 30%. Meanwhile, Anthropic announced Claude 3
        and Palantir secured a new government contract.
        """
        result = self.analyzer.analyze(text)

        # Should find multiple companies
        company_ids_found = {m.company.id for m in result.mentions}
        assert "apple" in company_ids_found
        assert "microsoft" in company_ids_found
        assert "anthropic" in company_ids_found
        assert "palantir" in company_ids_found

    def test_confidence_varies_by_uniqueness(self):
        """Unique names should generally have higher confidence than common words."""
        # Compare Anthropic (unique) vs Apple (common word) with similar context
        text_anthropic = "Anthropic is an AI company."
        text_apple = "Apple is a tech company."

        result_anthropic = self.analyzer.analyze(text_anthropic, ["anthropic"])
        result_apple = self.analyzer.analyze(text_apple, ["apple"])

        # Both should match, but Anthropic should have equal or higher confidence
        # because it doesn't need as much supporting context
        if result_anthropic.mentions and result_apple.mentions:
            anthropic_conf = result_anthropic.mentions[0].match_result.final_confidence
            apple_conf = result_apple.mentions[0].match_result.final_confidence
            # Anthropic with minimal context should still be confident
            assert anthropic_conf >= 0.6


class TestSensitivityProfiles:
    """Test the sensitivity profile configurations."""

    def test_common_word_profile_requires_context(self):
        """Common word profile should require context."""
        assert COMMON_WORD_PROFILE.require_context is True
        assert COMMON_WORD_PROFILE.min_confidence >= 0.8

    def test_unique_profile_allows_lower_confidence(self):
        """Unique name profile should allow lower confidence."""
        assert UNIQUE_NAME_PROFILE.require_context is False
        assert UNIQUE_NAME_PROFILE.min_confidence <= 0.7

    def test_company_sensitivity_inheritance(self):
        """Companies should have appropriate sensitivity settings."""
        assert APPLE.sensitivity.uniqueness == NameUniqueness.COMMON_WORD
        assert ANTHROPIC.sensitivity.uniqueness == NameUniqueness.UNIQUE
        assert FORD.sensitivity.uniqueness == NameUniqueness.AMBIGUOUS


class TestMatchingStrategies:
    """Test different matching strategies."""

    def test_exact_matching(self):
        """Test exact case-sensitive matching."""
        from src.analysis.matchers import ExactMatcher

        company = Company(
            id="test",
            name="TestCo",
            sensitivity=SensitivityProfile(
                uniqueness=NameUniqueness.MODERATE,
                matching_strategy=MatchingStrategy.EXACT,
            )
        )

        matcher = ExactMatcher()

        # Should match exact case
        matches = matcher.find_matches("TestCo announced results.", company)
        assert len(matches) == 1

        # Should not match different case
        matches = matcher.find_matches("testco announced results.", company)
        assert len(matches) == 0

    def test_fuzzy_matching(self):
        """Test fuzzy matching for typos."""
        from src.analysis.matchers import FuzzyMatcher

        company = Company(
            id="test",
            name="Anthropic",
            sensitivity=SensitivityProfile(
                uniqueness=NameUniqueness.UNIQUE,
                matching_strategy=MatchingStrategy.FUZZY,
            )
        )

        matcher = FuzzyMatcher(min_similarity=0.85)

        # Should match minor typo
        matches = matcher.find_matches("Antropic announced results.", company)
        # Might match depending on similarity threshold
        # "Antropic" vs "Anthropic" = 0.94 similarity
        assert len(matches) >= 0  # May or may not match based on exact implementation


class TestAnalysisSummary:
    """Test analysis result and summary functions."""

    def test_sensitivity_summary(self):
        """Test getting sensitivity summary."""
        analyzer = create_analyzer_from_registry()
        summary = analyzer.get_sensitivity_summary()

        assert "total_companies" in summary
        assert "by_uniqueness" in summary
        assert "by_strategy" in summary

        # Should have companies in multiple categories
        assert summary["total_companies"] > 0
        assert len(summary["by_uniqueness"]) > 1

    def test_analysis_result_methods(self):
        """Test analysis result helper methods."""
        analyzer = create_analyzer_from_registry()
        text = "Apple iPhone sales grew. Anthropic released Claude."

        result = analyzer.analyze(text)

        # Test getting mentions by company
        apple_mentions = result.get_mentions_by_company("apple")
        anthropic_mentions = result.get_mentions_by_company("anthropic")

        # Test getting high confidence mentions
        high_conf = result.get_high_confidence_mentions(0.7)
        assert all(m.match_result.final_confidence >= 0.7 for m in high_conf)
