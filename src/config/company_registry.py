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
# BLACKHORN VENTURES PORTFOLIO COMPANIES
# =============================================================================

TRYCOFI = Company(
    id="trycofi",
    name="trycofi",
    aliases=["trycofi.com", "Trycofi"],
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

GOLIOTH = Company(
    id="golioth",
    name="Golioth",
    aliases=["Golioth Inc"],
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

COMMON_ENERGY = Company(
    id="common_energy",
    name="Common Energy",
    aliases=[],
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

APERIA = Company(
    id="aperia",
    name="Aperia",
    aliases=["Aperia Technologies"],
    sector="Transportation",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Josh Carter", "Carter"],
    ),
)

TOGGLE_ROBOTICS = Company(
    id="toggle_robotics",
    name="Toggle Robotics",
    aliases=["Toggle"],
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Daniel Blank", "Blank"],
    ),
)

DRAWBOARD = Company(
    id="drawboard",
    name="Drawboard",
    aliases=["Drawboard Pty Ltd"],
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Allistair Michener", "Michener"],
    ),
)

AMPERON = Company(
    id="amperon",
    name="Amperon",
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

FERO_LABS = Company(
    id="fero_labs",
    name="Fero Labs",
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Berk Birand", "Birand", "Alp Kucukelbir", "Kucukelbir"],
    ),
)

VECNA_ROBOTICS = Company(
    id="vecna_robotics",
    name="Vecna Robotics",
    aliases=["Vecna Robotics, Inc.", "Vecna"],
    sector="Supply Chain / Logistics",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Karl Iagnemma", "Iagnemma"],
    ),
)

ETHIC = Company(
    id="ethic",
    name="Ethic",
    aliases=["ethicinvesting.com", "Ethic Investing"],
    sector="Financial Services",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Johny Mair", "Mair"],
    ),
)

KING_ENERGY = Company(
    id="king_energy",
    name="King Energy",
    aliases=["King Energy Inc"],
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

NEAR_SPACE_LABS = Company(
    id="near_space_labs",
    name="Near Space Labs",
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

SAFEHUB = Company(
    id="safehub",
    name="Safehub",
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Andy Thompson", "Thompson"],
    ),
)

ALICE_TECHNOLOGIES = Company(
    id="alice_technologies",
    name="ALICE Technologies",
    aliases=["ALICE"],
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["René Markos", "Markos"],
    ),
)

RAILVISION = Company(
    id="railvision",
    name="RailVision Analytics",
    aliases=["RailVision"],
    sector="Transportation",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

HYPERFRAME = Company(
    id="hyperframe",
    name="Hyperframe",
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

LATENT_AI = Company(
    id="latent_ai",
    name="Latent AI",
    aliases=["Latent AI, Inc."],
    sector="Artificial Intelligence",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

FORMIC = Company(
    id="formic",
    name="Formic",
    aliases=["Formic Technologies", "Formic Technologies Inc"],
    sector="Supply Chain / Logistics",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

FUTUREPROOF = Company(
    id="futureproof",
    name="FutureProof",
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

METABASE_Q = Company(
    id="metabase_q",
    name="Metabase Q",
    aliases=["Metabase"],
    sector="Cybersecurity",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

ENERGY_WEB = Company(
    id="energy_web",
    name="Energy Web",
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Jesse Morris", "Morris"],
    ),
)

SAFESITE = Company(
    id="safesite",
    name="Safesite",
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Peter Grant", "Leigh Appel", "Appel"],
    ),
)

CLIMATEAI = Company(
    id="climateai",
    name="ClimateAi",
    aliases=["ClimateAi inc", "Climate AI"],
    sector="Artificial Intelligence",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Himanshu"],
    ),
)

CYTOVALE = Company(
    id="cytovale",
    name="Cytovale",
    sector="Healthcare",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Ajay Shah", "Shah"],
    ),
)

ELECTRIC_ERA = Company(
    id="electric_era",
    name="Electric Era",
    aliases=["Electric Era Technologies", "Electric Era Technologies Inc"],
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

RIDEPANDA = Company(
    id="ridepanda",
    name="Ridepanda",
    sector="Transportation",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

BUZZ_SOLUTIONS = Company(
    id="buzz_solutions",
    name="Buzz Solutions",
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Kaitlyn Albertoli", "Albertoli", "Vik Hyat", "Hyat"],
    ),
)

OTONOMI = Company(
    id="otonomi",
    name="OTONOMI",
    sector="Supply Chain / Logistics",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

VEERUM = Company(
    id="veerum",
    name="VEERUM",
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["David Lod", "Lod"],
    ),
)

ECOWORKS = Company(
    id="ecoworks",
    name="ecoworks",
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

GREENLIGHT_AI = Company(
    id="greenlight_ai",
    name="GreenLight.ai",
    aliases=["GreenLight"],
    sector="Artificial Intelligence",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

RHUMBIX = Company(
    id="rhumbix",
    name="Rhumbix",
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Zachary Scheel", "Scheel"],
    ),
)

DEXTERITY = Company(
    id="dexterity",
    name="Dexterity",
    sector="Supply Chain / Logistics",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Samir Menon", "Menon"],
    ),
)

WUNDER = Company(
    id="wunder",
    name="Wunder",
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Dave Reiss", "Reiss"],
    ),
)

OPTERA = Company(
    id="optera",
    name="Optera",
    sector="Energy",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

ONEPOINTONE = Company(
    id="onepointone",
    name="OnePointOne",
    sector="Agriculture",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["John Bertram", "Samuel Bertram", "Bertram"],
    ),
)

DWELLSY = Company(
    id="dwellsy",
    name="Dwellsy",
    sector="Real Estate",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Jonas Bordo", "Bordo"],
    ),
)

GRID_RASTER = Company(
    id="grid_raster",
    name="Grid Raster",
    aliases=["Grid Raster Inc.", "Grid Raster Inc"],
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Rishi Ranjan", "Ranjan"],
    ),
)

SUSTAINMENT = Company(
    id="sustainment",
    name="Sustainment Technologies",
    aliases=["Sustainment Technologies Inc"],
    sector="Supply Chain / Logistics",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

AGERPOINT = Company(
    id="agerpoint",
    name="Agerpoint",
    sector="Agriculture",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Andrew Nash", "Nash"],
    ),
)

ULTRA_HIGH_MATERIALS = Company(
    id="ultra_high_materials",
    name="Ultra High Materials",
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Jonathan Cool", "Cool"],
    ),
)

DATCH = Company(
    id="datch",
    name="Datch",
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Mark Fosdike", "Fosdike"],
    ),
)

QUOTETOME = Company(
    id="quotetome",
    name="QuoteToMe",
    aliases=["QuoteToMe Inc"],
    sector="Construction",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

THINKLABS = Company(
    id="thinklabs",
    name="Think Labs",
    aliases=["ThinkLabs", "ThinkLabs AI"],
    sector="Artificial Intelligence",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

FORESIGHT_GROUP = Company(
    id="foresight_group",
    name="Foresight Group",
    aliases=["Foresight Group Inc"],
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

SUPPLYSHIFT = Company(
    id="supplyshift",
    name="SupplyShift",
    sector="Supply Chain / Logistics",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Jamie Barsimantov", "Barsimantov"],
    ),
)

CIRCUIT_MIND = Company(
    id="circuit_mind",
    name="Circuit Mind",
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

ARTIC = Company(
    id="artic",
    name="Artic",
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Tom Darlow", "Darlow"],
    ),
)

LAYER9 = Company(
    id="layer9",
    name="layer9.ai",
    aliases=["layer9", "Layer9"],
    sector="Artificial Intelligence",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

ALPHALEDGER = Company(
    id="alphaledger",
    name="Alphaledger",
    sector="Financial Services",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

ARX_ALLIANCE = Company(
    id="arx_alliance",
    name="ARX Alliance",
    aliases=["ARX"],
    sector="Industrial Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=[],
    ),
)

BATUTA = Company(
    id="batuta",
    name="Batuta",
    sector="Supply Chain / Logistics",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Mauricio Benavides", "Benavides"],
    ),
)

ATOMSCALE = Company(
    id="atomscale",
    name="Atomscale",
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Chris Price", "Jason Munro", "Munro"],
    ),
)

TRISTAR_AI = Company(
    id="tristar_ai",
    name="Tristar Ai",
    aliases=["Tristar AI", "TriStar"],
    sector="Transportation",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Salem Karani", "Karani", "Jack Liu"],
    ),
)

LEMURIAN_LABS = Company(
    id="lemurian_labs",
    name="Lemurian Labs",
    sector="Technology",
    sensitivity=replace(
        UNIQUE_NAME_PROFILE,
        context_keywords=["Jay Dawani", "Dawani"],
    ),
)

SWAY = Company(
    id="sway",
    name="Sway",
    sector="Industrial Technology",
    sensitivity=_with_context(
        COMMON_WORD_PROFILE,
        keywords=["Eric Wimer", "Wimer", "Kristian Zak", "Zak",
                  "packaging", "seaweed", "sustainable"],
        negative=["dance", "influence", "political sway", "opinion"],
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
    # Blackhorn Ventures portfolio
    "trycofi": TRYCOFI,
    "golioth": GOLIOTH,
    "common_energy": COMMON_ENERGY,
    "aperia": APERIA,
    "toggle_robotics": TOGGLE_ROBOTICS,
    "drawboard": DRAWBOARD,
    "amperon": AMPERON,
    "fero_labs": FERO_LABS,
    "vecna_robotics": VECNA_ROBOTICS,
    "ethic": ETHIC,
    "king_energy": KING_ENERGY,
    "near_space_labs": NEAR_SPACE_LABS,
    "safehub": SAFEHUB,
    "alice_technologies": ALICE_TECHNOLOGIES,
    "railvision": RAILVISION,
    "hyperframe": HYPERFRAME,
    "latent_ai": LATENT_AI,
    "formic": FORMIC,
    "futureproof": FUTUREPROOF,
    "metabase_q": METABASE_Q,
    "energy_web": ENERGY_WEB,
    "safesite": SAFESITE,
    "climateai": CLIMATEAI,
    "cytovale": CYTOVALE,
    "electric_era": ELECTRIC_ERA,
    "ridepanda": RIDEPANDA,
    "buzz_solutions": BUZZ_SOLUTIONS,
    "otonomi": OTONOMI,
    "veerum": VEERUM,
    "ecoworks": ECOWORKS,
    "greenlight_ai": GREENLIGHT_AI,
    "rhumbix": RHUMBIX,
    "dexterity": DEXTERITY,
    "wunder": WUNDER,
    "optera": OPTERA,
    "onepointone": ONEPOINTONE,
    "dwellsy": DWELLSY,
    "grid_raster": GRID_RASTER,
    "sustainment": SUSTAINMENT,
    "agerpoint": AGERPOINT,
    "ultra_high_materials": ULTRA_HIGH_MATERIALS,
    "datch": DATCH,
    "quotetome": QUOTETOME,
    "thinklabs": THINKLABS,
    "foresight_group": FORESIGHT_GROUP,
    "supplyshift": SUPPLYSHIFT,
    "circuit_mind": CIRCUIT_MIND,
    "artic": ARTIC,
    "layer9": LAYER9,
    "alphaledger": ALPHALEDGER,
    "arx_alliance": ARX_ALLIANCE,
    "batuta": BATUTA,
    "atomscale": ATOMSCALE,
    "tristar_ai": TRISTAR_AI,
    "lemurian_labs": LEMURIAN_LABS,
    "sway": SWAY,
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
