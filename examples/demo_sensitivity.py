#!/usr/bin/env python3
"""
Demonstration of company-aware sensitivity analysis.

This script shows how different companies are handled based on
their name uniqueness - common words like "Apple" require more
context than unique names like "Anthropic".
"""

import sys
sys.path.insert(0, '.')

from src.analysis.sensitivity import create_analyzer_from_registry
from src.config.company_registry import get_companies_by_uniqueness
from src.config.companies import NameUniqueness


def print_header(title: str):
    """Print a formatted header."""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def print_match_details(mention):
    """Print details about a match."""
    print(f"\n  Company: {mention.company.name} ({mention.company.id})")
    print(f"  Matched text: '{mention.match_result.match.text}'")
    print(f"  Uniqueness: {mention.company.sensitivity.uniqueness.value}")
    print(f"  Strategy: {mention.company.sensitivity.matching_strategy.value}")
    print(f"  Confidence: {mention.match_result.final_confidence:.2f}")
    print(f"  Valid: {mention.match_result.is_valid}")
    if mention.match_result.context_keywords_found:
        print(f"  Context keywords: {mention.match_result.context_keywords_found}")
    if mention.match_result.negative_keywords_found:
        print(f"  Negative keywords: {mention.match_result.negative_keywords_found}")
    print(f"  Explanation: {mention.match_result.explanation}")


def demo_common_word_companies():
    """Demonstrate handling of common-word company names."""
    print_header("COMMON WORD COMPANIES")
    print("\nCompanies with names that are common English words require")
    print("stricter matching with supporting context.")

    analyzer = create_analyzer_from_registry()

    # Apple in tech context - should match
    print("\n--- Apple (Tech Context) ---")
    text1 = "Apple reported record iPhone sales. AAPL stock jumped 5% in after-hours trading."
    result1 = analyzer.analyze(text1, ["apple"])
    print(f"Text: {text1}")
    print(f"Matches found: {len(result1.mentions)}")
    for m in result1.mentions:
        print_match_details(m)

    # Apple in fruit context - should NOT match
    print("\n--- Apple (Fruit Context) ---")
    text2 = "I picked a fresh apple from the orchard. Apple pie is my favorite dessert."
    result2 = analyzer.analyze(text2, ["apple"])
    print(f"Text: {text2}")
    print(f"Valid matches: {result2.valid_matches}")
    print(f"Rejected matches: {result2.rejected_matches}")

    # Amazon in e-commerce context - should match
    print("\n--- Amazon (E-commerce Context) ---")
    text3 = "Amazon Prime membership grew 20%. AWS cloud revenue exceeded expectations."
    result3 = analyzer.analyze(text3, ["amazon"])
    print(f"Text: {text3}")
    print(f"Matches found: {len(result3.mentions)}")
    for m in result3.mentions:
        print_match_details(m)

    # Amazon in nature context - should NOT match
    print("\n--- Amazon (Nature Context) ---")
    text4 = "The Amazon rainforest is crucial for the planet's ecosystem."
    result4 = analyzer.analyze(text4, ["amazon"])
    print(f"Text: {text4}")
    print(f"Valid matches: {result4.valid_matches}")
    print(f"Rejected matches: {result4.rejected_matches}")


def demo_unique_name_companies():
    """Demonstrate handling of unique company names."""
    print_header("UNIQUE NAME COMPANIES")
    print("\nCompanies with distinctive names can use relaxed matching")
    print("since false positives are rare.")

    analyzer = create_analyzer_from_registry()

    # Anthropic with minimal context - should still match
    print("\n--- Anthropic (Minimal Context) ---")
    text1 = "Anthropic announced a new product today."
    result1 = analyzer.analyze(text1, ["anthropic"])
    print(f"Text: {text1}")
    print(f"Matches found: {len(result1.mentions)}")
    for m in result1.mentions:
        print_match_details(m)

    # Anthropic with rich context - higher confidence
    print("\n--- Anthropic (Rich Context) ---")
    text2 = "Anthropic's Claude AI model shows improvements in safety. CEO Dario Amodei discussed the LLM advances."
    result2 = analyzer.analyze(text2, ["anthropic"])
    print(f"Text: {text2}")
    print(f"Matches found: {len(result2.mentions)}")
    for m in result2.mentions:
        print_match_details(m)

    # Palantir with minimal context
    print("\n--- Palantir (Minimal Context) ---")
    text3 = "Palantir secured a new contract."
    result3 = analyzer.analyze(text3, ["palantir"])
    print(f"Text: {text3}")
    print(f"Matches found: {len(result3.mentions)}")
    for m in result3.mentions:
        print_match_details(m)


def demo_ambiguous_names():
    """Demonstrate handling of ambiguous company names."""
    print_header("AMBIGUOUS NAME COMPANIES")
    print("\nNames that could refer to multiple entities need context")
    print("but not as strict as common words.")

    analyzer = create_analyzer_from_registry()

    # Ford with automotive context - should match
    print("\n--- Ford (Automotive Context) ---")
    text1 = "Ford F-150 sales lead the truck market. The EV Mustang is gaining traction."
    result1 = analyzer.analyze(text1, ["ford"])
    print(f"Text: {text1}")
    print(f"Matches found: {len(result1.mentions)}")
    for m in result1.mentions:
        print_match_details(m)

    # Ford as person's name - should NOT match
    print("\n--- Ford (Person's Name Context) ---")
    text2 = "Harrison Ford will star in the new film. Gerald Ford was the 38th president."
    result2 = analyzer.analyze(text2, ["ford"])
    print(f"Text: {text2}")
    print(f"Valid matches: {result2.valid_matches}")
    print(f"Rejected matches: {result2.rejected_matches}")


def demo_multi_company_analysis():
    """Demonstrate analyzing for multiple companies at once."""
    print_header("MULTI-COMPANY ANALYSIS")
    print("\nAnalyzing a single piece of text for multiple companies.")

    analyzer = create_analyzer_from_registry()

    text = """
    Tech earnings season is in full swing. Apple reported strong iPhone demand,
    while Microsoft Azure growth exceeded 30%. In AI news, Anthropic released
    Claude 3 with improved capabilities, and Palantir announced a major defense
    contract. Meanwhile, Ford's EV sales doubled year-over-year.
    """

    print(f"\nText:\n{text}")

    result = analyzer.analyze(text)

    print(f"\n--- Results ---")
    print(f"Companies checked: {len(result.companies_checked)}")
    print(f"Total matches found: {result.total_matches_found}")
    print(f"Valid matches: {result.valid_matches}")
    print(f"Rejected matches: {result.rejected_matches}")

    print("\n--- Valid Mentions ---")
    for mention in result.mentions:
        print(f"\n  {mention.company.name}:")
        print(f"    Confidence: {mention.match_result.final_confidence:.2f}")
        print(f"    Uniqueness: {mention.company.sensitivity.uniqueness.value}")


def demo_sensitivity_summary():
    """Show summary of sensitivity configurations."""
    print_header("SENSITIVITY CONFIGURATION SUMMARY")

    analyzer = create_analyzer_from_registry()
    summary = analyzer.get_sensitivity_summary()

    print(f"\nTotal companies monitored: {summary['total_companies']}")

    print("\nBy Name Uniqueness:")
    for uniqueness, count in sorted(summary['by_uniqueness'].items()):
        print(f"  {uniqueness}: {count} companies")

    print("\nBy Matching Strategy:")
    for strategy, count in sorted(summary['by_strategy'].items()):
        print(f"  {strategy}: {count} companies")

    print("\n--- Companies by Uniqueness Category ---")
    for uniqueness in NameUniqueness:
        companies = get_companies_by_uniqueness(uniqueness)
        if companies:
            print(f"\n{uniqueness.value.upper()}:")
            for c in companies[:5]:  # Show first 5
                print(f"  - {c.name} (min_conf: {c.sensitivity.min_confidence})")
            if len(companies) > 5:
                print(f"  ... and {len(companies) - 5} more")


def main():
    """Run all demonstrations."""
    print("\n" + "#" * 60)
    print("#  COMPANY-AWARE SENSITIVITY ANALYSIS DEMO")
    print("#" * 60)

    demo_sensitivity_summary()
    demo_common_word_companies()
    demo_unique_name_companies()
    demo_ambiguous_names()
    demo_multi_company_analysis()

    print("\n" + "=" * 60)
    print(" DEMO COMPLETE")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()
