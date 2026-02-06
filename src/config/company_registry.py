"""
Company registry with pre-configured sensitivity profiles.

This registry contains company definitions with appropriate sensitivity
settings based on name uniqueness. Companies with common-word names
require stricter matching to avoid false positives.
"""

from .companies import (
    Company,
    SensitivityProfile,
    NameUniqueness,
    MatchingStrategy,
    COMMON_WORD_PROFILE,
    AMBIGUOUS_NAME_PROFILE,
    MODERATE_PROFILE,
    UNIQUE_NAME_PROFILE,
)
from dataclasses import replace


def _with_context(profile: SensitivityProfile, keywords: list[str], negative: list[str] = None) -> SensitivityProfile:
    """Create a profile copy with specific context keywords."""
    return replace(
        profile,
        context_keywords=keywords,
        negative_keywords=negative or [],
    )


# =============================================================================
# COMMON WORD COMPANIES - Require strict matching with context
# =============================================================================

APPLE = Company(
    id="apple",
    name="Apple",
    ticker="AAPL",
    aliases=["Apple Inc", "Apple Inc.", "Apple Computer"],
    sector="Technology",
    sensitivity=_with_context(
        COMMON_WORD_PROFILE,
        keywords=["iPhone", "iPad", "Mac", "iOS", "App Store", "Tim Cook", "Cupertino",
                  "tech", "technology", "stock", "shares", "AAPL", "Silicon Valley"],
        negative=["fruit", "orchard", "pie", "cider", "tree", "recipe", "cooking"],
    ),
)

TARGET = Company(
    id="target",
    name="Target",
    ticker="TGT",
    aliases=["Target Corp", "Target Corporation"],
    sector="Retail",
    sensitivity=_with_context(
        COMMON_WORD_PROFILE,
        keywords=["retail", "store", "shopping", "TGT", "Minneapolis", "discount",
                  "Walmart", "retailer", "quarterly", "earnings"],
        negative=["aim", "goal", "objective", "shooting", "archery", "bullseye", "military"],
    ),
)

AMAZON = Company(
    id="amazon",
    name="Amazon",
    ticker="AMZN",
    aliases=["Amazon.com", "Amazon Inc", "Amazon Web Services", "AWS"],
    sector="Technology",
    sensitivity=_with_context(
        COMMON_WORD_PROFILE,
        keywords=["AWS", "Prime", "Bezos", "Jassy", "e-commerce", "cloud", "AMZN",
                  "Seattle", "Alexa", "Kindle", "retail", "tech"],
        negative=["river", "rainforest", "jungle", "Brazil", "South America", "ecosystem"],
    ),
)

DELTA = Company(
    id="delta",
    name="Delta",
    ticker="DAL",
    aliases=["Delta Air Lines", "Delta Airlines"],
    sector="Airlines",
    sensitivity=_with_context(
        COMMON_WORD_PROFILE,
        keywords=["airline", "flight", "aviation", "DAL", "Atlanta", "carrier",
                  "passengers", "routes", "airport"],
        negative=["math", "change", "difference", "Greek", "variable", "faucet"],
    ),
)

VISA = Company(
    id="visa",
    name="Visa",
    ticker="V",
    aliases=["Visa Inc"],
    sector="Financial Services",
    sensitivity=_with_context(
        COMMON_WORD_PROFILE,
        keywords=["credit card", "payment", "Mastercard", "transactions", "fintech",
                  "processing", "debit", "merchant"],
        negative=["immigration", "passport", "travel document", "embassy", "consulate"],
    ),
)

ORACLE = Company(
    id="oracle",
    name="Oracle",
    ticker="ORCL",
    aliases=["Oracle Corp", "Oracle Corporation"],
    sector="Technology",
    sensitivity=_with_context(
        COMMON_WORD_PROFILE,
        keywords=["database", "cloud", "software", "Larry Ellison", "ORCL", "Java",
                  "enterprise", "tech"],
        negative=["prophecy", "fortune", "mystic", "ancient", "Delphi"],
    ),
)

RESILIENCE = Company(
    id="resilience",
    name="Resilience",
    ticker=None,
    aliases=["Resilience Investments"],
    sector="Real Estate / Climate Finance",
    sensitivity=SensitivityProfile(
        uniqueness=NameUniqueness.COMMON_WORD,
        matching_strategy=MatchingStrategy.STRICT,
        min_confidence=0.65,
        require_context=True,
        context_window=50,
        context_keywords=["Jay Lipman", "Lipman", "Hunter Maats", "Maats",
                          "Ameet Konkar", "Konkar", "Andy Boyum", "Boyum",
                          "Resilience Investments"],
        negative_keywords=["emotional", "psychological", "mental health", "self-help",
                           "therapy", "coping", "trauma", "wellness"],
    ),
)


# =============================================================================
# AMBIGUOUS NAME COMPANIES - Names that could refer to multiple entities
# =============================================================================

MORGAN_STANLEY = Company(
    id="morgan_stanley",
    name="Morgan Stanley",
    ticker="MS",
    aliases=["MS"],
    sector="Financial Services",
    sensitivity=_with_context(
        AMBIGUOUS_NAME_PROFILE,
        keywords=["bank", "investment", "Wall Street", "wealth management", "trading",
                  "financial", "securities", "broker"],
        negative=[],
    ),
)

GOLDMAN = Company(
    id="goldman_sachs",
    name="Goldman Sachs",
    ticker="GS",
    aliases=["Goldman", "GS"],
    sector="Financial Services",
    sensitivity=_with_context(
        AMBIGUOUS_NAME_PROFILE,
        keywords=["bank", "investment", "Wall Street", "trading", "financial",
                  "securities", "IPO", "M&A"],
        negative=[],
    ),
)

FORD = Company(
    id="ford",
    name="Ford",
    ticker="F",
    aliases=["Ford Motor", "Ford Motor Company"],
    sector="Automotive",
    sensitivity=_with_context(
        AMBIGUOUS_NAME_PROFILE,
        keywords=["car", "auto", "vehicle", "truck", "F-150", "Mustang", "Detroit",
                  "automotive", "EV", "electric"],
        negative=["Harrison", "Gerald", "president", "river crossing"],
    ),
)

CHASE = Company(
    id="jpmorgan_chase",
    name="JPMorgan Chase",
    ticker="JPM",
    aliases=["JP Morgan", "JPMorgan", "Chase", "Chase Bank"],
    sector="Financial Services",
    sensitivity=_with_context(
        AMBIGUOUS_NAME_PROFILE,
        keywords=["bank", "banking", "financial", "Jamie Dimon", "Wall Street",
                  "credit card", "mortgage"],
        negative=["chase scene", "car chase", "pursuit"],
    ),
)


# =============================================================================
# MODERATE UNIQUENESS COMPANIES - Well-known names with some overlap potential
# =============================================================================

MICROSOFT = Company(
    id="microsoft",
    name="Microsoft",
    ticker="MSFT",
    aliases=["MSFT", "MS"],
    sector="Technology",
    sensitivity=replace(
        MODERATE_PROFILE,
        context_keywords=["Windows", "Azure", "Office", "Satya Nadella", "Xbox",
                          "cloud", "software", "Teams", "LinkedIn", "GitHub"],
    ),
)

GOOGLE = Company(
    id="google",
    name="Google",
    ticker="GOOGL",
    aliases=["Alphabet", "GOOGL", "GOOG"],
    sector="Technology",
    sensitivity=replace(
        MODERATE_PROFILE,
        context_keywords=["search", "Android", "Chrome", "YouTube", "Sundar Pichai",
                          "advertising", "cloud", "AI", "Gemini"],
    ),
)

META = Company(
    id="meta",
    name="Meta",
    ticker="META",
    aliases=["Meta Platforms", "Facebook"],
    sector="Technology",
    sensitivity=_with_context(
        MODERATE_PROFILE,
        keywords=["Facebook", "Instagram", "WhatsApp", "Zuckerberg", "social media",
                  "Threads", "VR", "metaverse", "advertising"],
        negative=["metadata", "meta-analysis", "meta tag", "metamorphosis"],
    ),
)

TESLA = Company(
    id="tesla",
    name="Tesla",
    ticker="TSLA",
    aliases=["TSLA"],
    sector="Automotive",
    sensitivity=replace(
        MODERATE_PROFILE,
        context_keywords=["EV", "electric vehicle", "Musk", "Elon", "autonomous",
                          "battery", "Gigafactory", "Model S", "Model 3", "Model Y"],
    ),
)

NETFLIX = Company(
    id="netflix",
    name="Netflix",
    ticker="NFLX",
    aliases=["NFLX"],
    sector="Entertainment",
    sensitivity=replace(
        MODERATE_PROFILE,
        context_keywords=["streaming", "subscribers", "content", "shows", "movies",
                          "originals", "Reed Hastings"],
    ),
)


# =============================================================================
# UNIQUE NAME COMPANIES - Distinctive names with low false positive risk
# =============================================================================

ANTHROPIC = Company(
    id="anthropic",
    name="Anthropic",
    ticker=None,
    aliases=["Anthropic AI", "Anthropic PBC"],
    sector="Artificial Intelligence",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Claude", "AI", "safety", "Dario Amodei", "Daniela Amodei",
                          "artificial intelligence", "LLM", "foundation model"],
    ),
)

PALANTIR = Company(
    id="palantir",
    name="Palantir",
    ticker="PLTR",
    aliases=["Palantir Technologies", "PLTR"],
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["data", "analytics", "government", "Thiel", "Gotham",
                          "Foundry", "defense"],
    ),
)

SNOWFLAKE = Company(
    id="snowflake",
    name="Snowflake",
    ticker="SNOW",
    aliases=["Snowflake Inc", "SNOW"],
    sector="Technology",
    sensitivity=_with_context(
        UNIQUE_NAME_PROFILE,
        keywords=["data", "cloud", "warehouse", "analytics", "SNOW", "database",
                  "Slootman"],
        negative=["weather", "winter", "snow", "frozen", "Christmas"],
    ),
)

CROWDSTRIKE = Company(
    id="crowdstrike",
    name="CrowdStrike",
    ticker="CRWD",
    aliases=["CRWD", "Crowd Strike"],
    sector="Cybersecurity",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["security", "cybersecurity", "endpoint", "Falcon",
                          "threat", "breach"],
    ),
)

DATADOG = Company(
    id="datadog",
    name="Datadog",
    ticker="DDOG",
    aliases=["DDOG"],
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["monitoring", "observability", "cloud", "APM", "logs",
                          "infrastructure"],
    ),
)

MONGODB = Company(
    id="mongodb",
    name="MongoDB",
    ticker="MDB",
    aliases=["MDB", "Mongo"],
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["database", "NoSQL", "cloud", "Atlas", "document database"],
    ),
)

SPLUNK = Company(
    id="splunk",
    name="Splunk",
    ticker="SPLK",
    aliases=["SPLK"],
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["data", "security", "SIEM", "logs", "observability",
                          "machine data"],
    ),
)


# =============================================================================
# COMPANY REGISTRY
# =============================================================================

COMPANY_REGISTRY: dict[str, Company] = {
    # Common word companies
    "apple": APPLE,
    "target": TARGET,
    "amazon": AMAZON,
    "delta": DELTA,
    "visa": VISA,
    "oracle": ORACLE,
    "resilience": RESILIENCE,
    # Ambiguous name companies
    "morgan_stanley": MORGAN_STANLEY,
    "goldman_sachs": GOLDMAN,
    "ford": FORD,
    "jpmorgan_chase": CHASE,
    # Moderate uniqueness
    "microsoft": MICROSOFT,
    "google": GOOGLE,
    "meta": META,
    "tesla": TESLA,
    "netflix": NETFLIX,
    # Unique names
    "anthropic": ANTHROPIC,
    "palantir": PALANTIR,
    "snowflake": SNOWFLAKE,
    "crowdstrike": CROWDSTRIKE,
    "datadog": DATADOG,
    "mongodb": MONGODB,
    "splunk": SPLUNK,
}


def get_company(company_id: str) -> Company | None:
    """Get a company by ID."""
    return COMPANY_REGISTRY.get(company_id.lower())


def get_all_companies() -> list[Company]:
    """Get all registered companies."""
    return list(COMPANY_REGISTRY.values())


def get_companies_by_uniqueness(uniqueness: NameUniqueness) -> list[Company]:
    """Get all companies with a specific uniqueness classification."""
    return [
        c for c in COMPANY_REGISTRY.values()
        if c.sensitivity and c.sensitivity.uniqueness == uniqueness
    ]


def get_companies_by_sector(sector: str) -> list[Company]:
    """Get all companies in a specific sector."""
    return [
        c for c in COMPANY_REGISTRY.values()
        if c.sector and c.sector.lower() == sector.lower()
    ]
